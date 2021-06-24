import requests

url = "https://discord.com/api/v9/channels/857466994126618645/typing"

headers = {
  'authorization': 'ODUwNTg4ODUzMzc4NDgyMTg2.YNP1Jg.xA_tn5vc5eTLqLd-9_x98eRVXc8'
}

response = requests.request("POST", url, headers=headers)

print(response.text)