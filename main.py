import time
import requests

count = 0
url = "https://discord.com/api/v9/channels/857466994126618645/typing"
headers = {
  'authorization': ''
}

while True:
	response = requests.request("POST", url, headers=headers)
	if response.status_code != 204:
		print(response.text)
		print("Failed")
	else:
		count += 1
		print(f"Sent - {count}")