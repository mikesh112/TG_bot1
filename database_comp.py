import hashlib
import json
from main import user_name

with open('db.json') as f:  # open db
    db = json.load(f)  # user_id - file numbers

user_id = hashlib.md5(user_name.encode("utf-8")).hexdigest()  # get hash name = id

if user_id not in db:  # if new name - 1
    db[user_id] = 1
else:
    db[user_id] = db[user_id] + 1  # else add +1

with open('db.json', 'w') as f:  # update db
    json.dump(db, f)