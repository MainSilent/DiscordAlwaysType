from time import sleep
import requests
from os.path import exists

if(not exists("token")) :
	new_token_file = open("token", "w+")
	new_token_file.write(input("Enter your token: "))
	new_token_file.seek(0)
	token = new_token_file.read()
else:
	token_file = open("token", "r")
	token = token_file.read()

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
