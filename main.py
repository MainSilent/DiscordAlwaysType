from time import sleep
import requests
from os.path import exists

def token_file_create():
	token = input("Enter your token: ")
	if(token == ""):
		token_file_create()
	new_token_file = open("token", "w")
	new_token_file.write(token)
	return token

def token_file_read():
	token_file = open("token", "r")
	token = token_file.read()
	return token

if(not exists("token") or open("token", "r").read() == "") :
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
