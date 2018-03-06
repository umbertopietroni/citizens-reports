drop table if exists users;
create table users (
	id int(11) auto_increment primary key not null,
	phone_number char(20) default '',
	description char(50) default ''
);


drop table if exists issues;
create table issues (
	id int(11) auto_increment primary key not null,
	day date,
	time time,
	user_id int(11) not null,
	latitude decimal(10, 8), 
	longitude decimal(10, 8), 
	text text,
	category char(50) default '',
	status char(20) default 'NEW',
	classification_dict text default ''
);


drop table if exists images;
create table images (
	id int(11) auto_increment primary key not null,
	issue_id int(11) not null,
	filename varchar(500),
	category char(50) default '',
	classification_dict text default ''
);

