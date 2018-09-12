
import requests
import base64
url = 'http://79.137.175.13/submissions/1/'
headers = {'Authorization': 'Basic YWxsYWRpbjpvcGVuc2VzYW1l'}

r = requests.post(url, headers=headers)
url1 = 'http://79.137.175.13/submissions/super/duper/secret/'
print(base64.b64encode(b'galchonok:ktotama'))
header1 = {'Authorization': 'Basic Z2FsY2hvbm9rOmt0b3RhbWE='}
r1 = requests.put(url1, headers=header1)
with open('answer.txt', 'w') as f:
    f.write(r1.json()['answer'])