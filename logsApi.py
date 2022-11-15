using System;
using System.Net;
using System.Net.Http;
using System.Threading.Tasks;
using System.Collections.Generic;
using System.Text;
using System.Text.Json;

namespace LM_Logs_Code
{

    class LMLogsIngestExample
    {
        static void Main(string[] args)
        {
            //Run async request
            SubmitLMLogMessage().Wait();
        }
        static async Task SubmitLMLogMessage()
        {
            //Get current time in epoch
            long epoch = new DateTimeOffset(DateTime.UtcNow).ToUnixTimeMilliseconds();

            string message = "enter message content for logging to LM";

            //Create our POST content, _lm.resourceId must map to a LM resource using the specified key value pair
            var values = new Dictionary<string, object>
            {
                {"message", message},
                {"timestamp", epoch},
                {"_lm.resourceId", new Dictionary<string, string>()
                    {
                        {"system.hostname","enter lm device name you are mapping this log to"} //Make sure to set this to a valid system.hostname property for a device in LM
                    }
                },
                {"app_version","1.0"} //You can add optionally additional metadata properties that will be sent along with the ingested message
            };

            //Create envents array to store our log messages
            var events = new[] { values };

            //Serialize our events array into JSON
            var jsonObject = JsonSerializer.Serialize(events);
            var content = new StringContent(jsonObject.ToString(), Encoding.UTF8, "application/json");

            //Our LM portal credentials for authentication
            var accessKey = "enter lm access key";
            var accessId = "enter lm access id";
            var accountName = "enter lm account name";

            //Setup request headers and authentication
            var resourcePath = "/log/ingest";
            var requestVars = "POST" + epoch + jsonObject.ToString() + resourcePath;

            //Construct authorication LMv1 key
            var hmac = new System.Security.Cryptography.HMACSHA256();
            hmac.Key = System.Text.Encoding.UTF8.GetBytes(new System.Net.NetworkCredential("", accessKey).Password);
            var signatureBytes = hmac.ComputeHash(System.Text.Encoding.UTF8.GetBytes(requestVars));
            var signatureHex = System.BitConverter.ToString(signatureBytes).Replace("-", "");
            var signature = System.Convert.ToBase64String(System.Text.Encoding.UTF8.GetBytes(signatureHex.ToLower()));

            //Setup HttpClient and Request Headers
            var client = new HttpClient();
            var requestMessage = new HttpRequestMessage
            {
                Method = HttpMethod.Post,
                RequestUri = new Uri($"https://{accountName}.logicmonitor.com/rest{resourcePath}"),
                Headers = {
                    { HttpRequestHeader.Authorization.ToString(), $"LMv1 {accessId}:{signature}:{epoch}" },
                    { HttpRequestHeader.Accept.ToString(), "application/json" },
                    { "X-Version", "3" }
                },
                Content = new StringContent(jsonObject.ToString(), Encoding.UTF8, "application/json")
            };

            //Async POST request to ingest API
            var response = client.SendAsync(requestMessage).Result;
            var responseString = await response.Content.ReadAsStringAsync();

            //Write response
            Console.WriteLine(responseString);
        }
    }
}