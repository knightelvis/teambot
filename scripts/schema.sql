USE teambot;

DROP TABLE IF EXISTS Team;

/* Team table is to store basic team profile data.*/
CREATE TABLE Team(
	id BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	/* A team is a slack team */
	token VARCHAR(255), # slack access token for that team
	name VARCHAR(255),
	uri VARCHAR(255),
	email VARCHAR(255),
	owner VARCHAR(255), # an url points to the picture
	admin VARCHAR(255),
	register_time DATETIME
);


DROP TABLE IF EXISTS User;

/* User table is to store basic user profile data.*/
CREATE TABLE User(
	id BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	/* From Uber user profile data */
	token VARCHAR(255), # not sure how long the access token is in uber
	first_name VARCHAR(100),
	last_name VARCHAR(100),
	slack_id VARCHAR(255), # this is only unique within a team
	slack_username VARCHAR(255), # an url points to the picture
	team_uri VARCHAR(255),
	/* Our user data*/
	register_time DATETIME,
	status TINYINT /* 1 DELETED, 2 DEACTIVATED, 0 ACTIVE etc. */
);

DROP TABLE IF EXISTS Todo;

CREATE TABLE Todo (
	id BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	user_id BIGINT, # our unique id, not the slack user id
	from_user VARCHAR(255), # this is the slack user name
	create_time DATETIME, 
	due_time DATETIME,
	content VARCHAR(510), 
	status TINYINT, # 0 todo, 1 completed
	priority TINYINT # the lower the higher priority
);
