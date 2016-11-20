#!/usr/bin/python3

import sqlite3
import time


class DB_interactor:
	def __init__(self):
		self.current_day = 'Monday'

	def create_connect(self):
		con = sqlite3.connect('data_base.db')
		return con

	def close_connect(self, con):
		con.commit()
		con.close()

	def add_user(self, first_name, last_name, group, id):
		result = self.user_isregistred(id)
		con = self.create_connect()
		if result[0]:
			return result[1]
		else:
			try:
				with con:
					cur = con.cursor()
					cur.execute("INSERT INTO user(first_name, last_name, group_id, id) VALUES (?, ?, ?, ?)", (first_name, last_name, group, id))
					result = self.get_lesson_id_by_group_id(group)
					for i in result:
						cur.execute("INSERT INTO rating(lesson_id, id, rate) VALUES (?, ?, ?)", (int(i[0]), id, 0))
					con.commit()
					return self.user_isregistred(id)[1]
			except sqlite3.Error:
				return None

	def get_all_user_id(self):
		con = self.create_connect()
		cur = con.cursor()
		cur.execute("SELECT id FROM user");
		result = cur.fetchall()
		if not result:
			return None
		else:
			return result

	def get_lesson_id_by_group_id(self, group_id):
		con = self.create_connect()
		cur = con.cursor()
		cur.execute("SELECT s.lesson_id FROM schedule AS s INNER JOIN lesson AS l ON s.lesson_id = l.lesson_id WHERE group_id = ?", (str(group_id),))
		result = cur.fetchall()
		if not result:
			return None
		else:
			return result
		
	def user_isregistred(self, id):
		con = self.create_connect()
		try:
			with con:
				cur = con.cursor()
				cur.execute("SELECT id FROM user WHERE id = ?", (id, ))
				result = cur.fetchall()
				if not result:
					return (False, None)
				else:
					return (True, result[0][0])
		except sqlite3.Error:
			return (False, None)


	def get_user(self, id):
		result = self.user_isregistred(id)
		return result[1]

	'''______________________________________________________________________________________'''

	def rate_up(self, id, num):
		rating_id = self.get_rate_id(id, num)
		con = self.create_connect()
		cur = con.cursor()
		cur.execute("UPDATE rating SET rate = rate + 1 WHERE rating_id = ?", (rating_id,))
		con.commit()


	def get_rate_id(self, id, num):
		con = self.create_connect()
		cur = con.cursor()
		cur.execute("SELECT rating_id FROM rating INNER JOIN lesson ON lesson.lesson_id = rating.lesson_id WHERE num = ? AND id = ?", (num, id))
		result = cur.fetchall()
		if not result:
			return None
		else:
			return result[0][0]

	'''_______________________________________________________________________________________'''

	def mark_me(self, id, num):
		lesson_id = self.get_lesson_id(id, num)
		con = self.create_connect()
		cur = con.cursor()
		cur.execute("SELECT id, rate FROM rating WHERE lesson_id = ?", (lesson_id, ))
		result = cur.fetchall()
		if not result:
			return None
		else:
			return result

	def get_group_id_by_id(self, id):
		con = self.create_connect()
		cur = con.cursor()
		cur.execute("SELECT group_id FROM user WHERE id = ?", (id,))
		result = cur.fetchall()
		if not result:
			return None
		else:
			return result[0][0]

	def get_day_id_by_day(self, day):
		con = self.create_connect()
		cur = con.cursor()
		cur.execute("SELECT day_id FROM day WHERE day_name = ?", (day, ))
		result = cur.fetchall()
		if not result:
			return None
		else:
			return result[0][0]

	def get_lesson_id(self, id, num):
		group_id = self.get_group_id_by_id(id)
		day_id = self.get_day_id_by_day(self.current_day)
		con = self.create_connect()
		cur = con.cursor()
		group_id = str(group_id)
		day_id = str(day_id)
		cur.execute("SELECT schedule.lesson_id FROM schedule INNER JOIN lesson ON lesson.lesson_id = schedule.lesson_id WHERE num = ? AND group_id = ? AND day_id = ?", (num, group_id, day_id))
		result = cur.fetchall()
		print(result)
		if not result:
			return None
		else:
			return int(result[0][0])





