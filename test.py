import json
import datetime

account = 'account_1'
point = ''
with open('accounts.json', 'r') as f:
    file = json.load(f)


for key, v in file.items():
    if key == account:
        user_name = v['user_name']
        first_name = v['first_name']
        last_name = v['last_name']
        email = v['email']
        describe = v['describe']
        date_of_birth = v['date_of_birth']

print(describe)