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
	first_name VARCHAR(100),
	last_name VARCHAR(100),
	slack_userid VARCHAR(255), # this is only unique within a team
	slack_username VARCHAR(255), # an url points to the picture
	team_id BIGINT,
	team_uri VARCHAR(255),
	register_time DATETIME,
	status TINYINT /* 1 DELETED, 2 DEACTIVATED, 0 ACTIVE etc. */
);

DROP TABLE IF EXISTS Task;

CREATE TABLE Task (
	id BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	owner_id BIGINT, # our unique id, not the slack user id
	owner_first_name VARCHAR(100), # for easy use
	owner_slack_username VARCHAR(255),
	from_user VARCHAR(255), # this is the slack user name
	from_user_id VARCHAR(255), # this is the user id from the same slack team
	create_time DATETIME, 
	due_time DATETIME,
	content VARCHAR(510), 
	status TINYINT, # 0 todo, 1 completed, 2 deleted
	priority TINYINT # the lower the higher priority
);
