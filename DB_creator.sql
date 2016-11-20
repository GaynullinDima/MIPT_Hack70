CREATE TABLE user (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(255),
	last_name VARCHAR(255),
	group_id INTEGER
);

CREATE TABLE day (
	day_id INTEGER PRIMARY KEY AUTOINCREMENT,
	day_name VARCHAR(15)
);
INSERT INTO day (day_name) 
      VALUES ('Monday');
INSERT INTO day (day_name) 
      VALUES ('Tuesday');
INSERT INTO day (day_name) 
      VALUES ('Wednesday');
INSERT INTO day (day_name) 
      VALUES ('Thursday');
INSERT INTO day (day_name) 
      VALUES ('Friday');
INSERT INTO day (day_name) 
      VALUES ('Saturday');

CREATE TABLE course (
	course_id INTEGER PRIMARY KEY AUTOINCREMENT,
	course_type_id REFERENCES course_type(course_type_id),
	course_name VARCHAR(255)
);

CREATE TABLE course_type (
	course_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
	course_type_name VARCHAR(15)
);
INSERT INTO course_type (course_type_name) 
      VALUES ('lecture');
INSERT INTO course_type (course_type_name) 
      VALUES ('seminar');

CREATE TABLE lesson (
	lesson_id INTEGER PRIMARY KEY AUTOINCREMENT,
	course_id REFERENCES course(course_id),
	day_id REFERENCES day(day_id),
	num INTEGER
);

CREATE TABLE schedule (
	schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
	lesson_id REFERENCES lesson(lesson_id),
	group_id REFERENCES user(group_id)
);

CREATE TABLE rating (
	rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
	lesson_id REFERENCES lesson(lesson_id),
	user_id REFERENCES user(user_id),
	rate INTEGER 
);

