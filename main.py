from time import sleep
import requests

token = ''
channel_id = input("Enter desired channel id: ")

count = 0
url = f"https://discord.com/api/v9/channels/{channel_id}/typing"
headers = {
  'authorization': token
}

while True:
	response = requests.request("POST", url, headers=headers)
	if response.status_code != 204:
		print(f"Failed {response.text}")
	else:
		count += 1
		print(f"Sent - {count}")
	sleep(3)
