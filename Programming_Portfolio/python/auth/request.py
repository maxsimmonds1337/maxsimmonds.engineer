import requests
from requests.auth import HTTPBasicAuth

response = requests.get('https://api.github.com / user, ',
		auth = HTTPBasicAuth('user', 'pass'))

print(response)
