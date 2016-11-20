import sqlite3
import collections 
import time 
import db_interactor as db

db = db.DB_interactor()
current_day = time.strftime("%A")


print(db.user_isregistred(1))
print(db.add_user("vas", "pup", 416, 5))
print(db.get_user(1))
print(db.get_group_id_by_id(3))
print(db.mark_me(3, 3))
print(db.get_lesson_id_by_group_id(416))
