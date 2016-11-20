import sqlite3
import collections 
import time 
import db_interactor as db

db = db.DB_interactor()
current_day = time.strftime("%A")


print(db.user_isregistred("vas", "pup", 41, 3))
print(db.add_user("vas", "pup", 412, 4))
print(db.get_user("vas", "pup", 412, 3))
print(db.mark_me(3, 2))

