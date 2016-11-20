#!/usr/bin/python3

import sqlite3
import time


class DB_interactor:
	def __init__(self):
		self.current_day = time.strftime("%A")

	def create_connect(self):
		con = sqlite3.connect('our.db')
		return con

	def close_connect(self, con):
		con.commit()
		con.close()


	def add_user(self, first_name, last_name, group, id):
		result = user_isregistred(first_name, last_name, group)
		con = create_connect()
		if result[0]:
			return result[1]
		else:
			try:
				with con:
					cur = con.cursor()
					cur.execute("INSERT INTO user(first_name, last_name, group_id) VALUES (?, ?, ?, ?)", (first_name, last_name, group, id))
					con.commit()
					return user_isregistred(first_name, last_name, group)[1]
			except sqlite3.Error:
				return None

		
	def user_isregistred(self, first_name, last_name, group, id):
		con = create_connect()
		try:
			with con:
				cur = con.cursor()
				cur.execute("SELECT id FROM user WHERE first_name = ? AND last_name = ? AND group_id = ? AND id = ?", (first_name, last_name, group, id))
				result = cur.fetchall()
				if not result:
					return (False, None)
				else:
					return (True, result[0][0])
		except sqlite3.Error:
			return (False, None)


	def get_user(self, first_name, last_name, group, id):
		result = user_isresgistred(first_name, last_name, group, id)
		return result[1]

	'''______________________________________________________________________________________'''

	def rate_up(self, id, num):
		rating_id = get_rate_id(id, num)
		con = create_connect()
		cur = con.cursor()
		cur.execute("UPDATE rating SET rate = rate + 1 WHERE rating_id = ?", (rating_id,))
		con.commit()


	def get_rate_id(self, id, num):
		con = create_connect()
		cur = con.cursor()
		cur.execute("SELECT rating_id FROM rating INNER JOIN lesson ON lesson.lesson_id = rating.lesson_id WHERE num = ? AND id = ?", (num, id))
		result = cur.fetchall()
		if not result:
			return None
		else:
			return result[0][0]

	'''_______________________________________________________________________________________'''

	def mark_me(self, id, num):
		lesson_id = get_lesson_id(id, num)
		con = create_connect()
		cur = con.cursor()
		cur.execute("SELECT id, rate FROM rating WHERE lesson_id = ?", (lesson_id, ))
		result = cur.fetchall()
		if not result:
			return None
		else:
			return result

	def get_group_id_by_id(self, id):
		con = create_connect()
		cur = con.cursor()
		cur.execute("SELECT group_id FROM user WHERE id = ?", (id,))
		result = cur.fetchall()
		if not result:
			return None
		else:
			return result[0][0]

	def get_day_id_by_day(self, day):
		con = create_connect()
		cur = con.cursor()
		cur.execute("SELECT day_id FROM day WHERE day_name = ?", (day, ))
		result = cur.fetchall()
		if not result:
			return None
		else:
			return result[0][0]

	def get_lesson_id(self, id, num):
		group_id = get_group_id_by_id(id)
		day_id = get_day_id_by_day(current_day)
		con = create_connect()
		cur = con.cursor()
		cur.execute("SELECT lesson_id FROM schedule INNER JOIN lesson ON lesson.lesson_id = schedule.lesson_id WHERE num = ? AND group_id = ? AND day_id = ?", (num, group_id, day_id))
		result = cur.fetchall()
		if not result:
			return None
		else:
			return result[0][0]

