import json
import datetime

account = 'account_1'
point = ''
with open('accounts.json', 'r') as f:
    file = json.load(f)


for key, value in file.items():
    if key == account:
        point = value['login']


print(type(point))