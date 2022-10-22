from time import sleep
import requests
from os.path import exists


def token_file_create():
	token = ''
	while token == '':
		token = input("Enter your token: ")
		with open("token", "w") as f:
			f.write(token)
	return token


def token_file_read():
	with open("token", "r") as f:
		return f.read().strip()


if(not exists("token") or token_file_read() == ""):
	token = token_file_create()
else:
	token = token_file_read()

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
