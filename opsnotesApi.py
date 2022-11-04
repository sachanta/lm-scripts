#!/bin/env python3

import requests
import json
import hashlib
import base64
import time
import hmac

#Account Info: LogicMonitor recommends to NEVER hardcode the credentials. Instead, retrieve the values from a secure storage.
#Note: The below is provided for illustration purposes only.
AccessId = "<insert access id>"
AccessKey = "<insert access key>"
Company = 'analyticpartners'

#Request Info
httpVerb ='POST'
resourcePath = '/setting/opsnotes'
queryParams =''
data = '{"note":"deploy version 3.4.5","tags":[{"name":"relase-3.4.5"}],"scopes":[{"type":"deviceGroup","groupId":389}]}'

#Construct URL 
url = 'https://'+ Company +'.logicmonitor.com/santaba/rest' + resourcePath +queryParams

#Get current time in milliseconds
epoch = str(int(time.time() * 1000))

#Concatenate Request details
requestVars = httpVerb + epoch + data + resourcePath

# Construct signature
digest = hmac.new(
AccessKey.encode('utf-8'),
msg=requestVars.encode('utf-8'),
digestmod=hashlib.sha256).hexdigest()
signature = base64.b64encode(digest.encode('utf-8')).decode('utf-8')
# Construct headers
auth = 'LMv1 ' + AccessId + ':' + str(signature) + ':' + epoch
headers = {'Content-Type':'application/json','Authorization':auth}
# Make request
response = requests.post(url, data=data, headers=headers)
# Print status and body of response
print('Response Status:',response.status_code)
print('Response Body:',response.content)