import requests # pip install requests
import json     # pip install json

# Path of image (jpg/jpeg/png)
file = "fashion.jpg"

# url name
url = "https://fashion.recoqnitics.com/analyze"
accessKey = "18f38db58e2375790160"
secretKey = "f2c08046086c40ba811d5ff5fd46d26d9c0a4d78"

# access_key and secret_key
data = {'access_key': accessKey,
  'secret_key': secretKey}

filename = {'filename': open(file,'rb')}
r = requests.post(url, files = filename, data=data)
content = json.loads(r.content)
print(content)