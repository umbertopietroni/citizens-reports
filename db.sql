drop table if exists users;
create table users (
	id int(11) auto_increment primary key not null,
	user_id int(11) not null,
	channel char(20) default '', 
	phone_number char(20) default '',
	description char(50) default ''
);
create unique index users_idx0 on users(user_id, channel);


drop table if exists issues;
create table issues (
	id int(11) auto_increment primary key not null,
	day date,
	time time,
	user_id int(11) not null,
	msg_id int(11) not null,
	latitude decimal(10, 8), 
	longitude decimal(10, 8), 
	channel char(20) default '', 
	text text,
	category char(50) default '',
	status char(20) default 'NEW',
	classification_dict text default ''
);
create unique index issues_idx0 on issues(user_id, msg_id, channel);


drop table if exists images;
create table images (
	id int(11) auto_increment primary key not null,
	issue_id int(11) not null,
	filename varchar(500),
	category char(50) default '',
	classification_dict text default ''
);

