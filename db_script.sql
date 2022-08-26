create table users (
	id SERIAL,
	email varchar(200) default null,
	username varchar(200) default null,
	first_name varchar(45) default null,
	last_name varchar(45) default null,
	hashed_password varchar(45) default null,
	is_active boolean default null,
	primary key (id)
)

create table todo (
	id SERIAL,
	title varchar(200) default null,
	description varchar(200) default null,
	priority integer default null,
	complete boolean default null,
	user_id integer default null,
	primary key (id),
	foreign key (user_id) references users(id) 
)