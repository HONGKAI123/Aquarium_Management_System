drop database if exists aquarium;
create database aquarium;
use aquarium;

create table aquarist
	(st_ID		char(9),
     hashed_pw	binary(64),
     name		varchar(40),
     phone		char(9),
     email		varchar(40),
     primary key (st_ID)
    );
    
create table curator
	(st_ID		char(9),
     hashed_pw	binary(64),
     name		varchar(40),
     phone		char(9),
     email		varchar(40),
     primary key (st_ID)
    );
    
create table event_manager
	(st_ID		char(9),
     hashed_pw	binary(64),
     name		varchar(40),
     phone		char(9),
     email		varchar(40),
     primary key (st_ID)
    );
    
create table director
	(st_ID		char(9),
     hashed_pw	binary(64),
     name		varchar(40),
     phone		char(9),
     email		varchar(40),
     primary key (st_ID)
    );
    
create table facility
	(fa_ID		char(6),
     name		varchar(40),
     primary key (fa_ID)
     );

create table facility_maint
	(facility	char(6),
     maint_time	time,
     maint_status bool,
     foreign key (facility) references facility(fa_id) on delete cascade
     );
	
create table maintain
	(staff		char(9),
     facility	char(6),
     foreign key (staff) references aquarist(st_ID),
     foreign key (facility) references facility(fa_ID)
	);

create table animal
	(an_ID		char(6),
     name		varchar(40),
     species	varchar(40),
     status		int,
     curator	char(9),
     habitat	char(6),
     primary key (an_ID),
     foreign key (curator) references curator(st_ID) on delete no action,
     foreign key (habitat) references facility(fa_ID) on delete no action
     );
     
create table event
	(ev_ID		char(6),
	 title		varchar(40),
     type		enum('exhibit', 'performance'),
     facility	char(6),
     overseer	char(9),
     primary key (ev_ID),
     foreign key (facility) references facility(fa_ID) on delete no action,
     foreign key (overseer) references event_manager(st_ID) on delete no action
	);

create table event_instance
	(event		char(6),
     date		date,
     attendance	int,
     foreign key (event) references event(ev_ID) on delete cascade
	);
    
create table work_on
	(event		char(6),
     staff		char(9),
     foreign key (event) references event(ev_ID) on delete cascade,
     foreign key (staff) references aquarist(st_ID) on delete cascade
	);
    
create table participate
	(event		char(6),
     animal		char(6),
     foreign key (event) references event(ev_ID) on delete cascade,
     foreign key (animal) references animal(an_ID) on delete cascade
	);


insert into director values ('517465989', md5(517465989), 'Farnsworth', '5551234', 'farnsworth@aquarium.com');

insert into event_manager values ('243910037', md5(243910037), 'Leela', '5551235', 'leela@aquarium.com');
insert into event_manager values ('218363685', md5(218363685), 'Hermes', '5551236', 'hermes@aquarium.com');

insert into curator values ('736289249', md5(736289249), 'Zoidberg', '5551237', 'zoidberg@aquarium.com');
insert into curator values ('705628448', md5(705628448), 'Amy', '5551238', 'amy@aquarium.com');

insert into aquarist values ('914191383', md5(914191383), 'Fry', '5551239', 'fry@aquarium.com');
insert into aquarist values ('143705926', md5(143705926), 'Bender', '5551240', 'bender@aquarium.com');
insert into aquarist values ('315400662', md5(315400662), 'Scruffy', '5551241', 'scruffy@aquarium.com');
insert into aquarist values ('888748129', md5(888748129), 'Cubert', '5551242', 'cubert@aquarium.com');
insert into aquarist values ('689620370', md5(689620370), 'Zapp', '5551243', 'zapp@aquarium.com');
insert into aquarist values ('504236312', md5(504236312), 'Kif', '5551244', 'kif@aquarium.com');
insert into aquarist values ('987153744', md5(987153744), 'Elzar', '5551245', 'elzar@aquarium.com');
insert into aquarist values ('608059001', md5(608059001), 'Flexo', '5551246', 'flexo@aquarium.com');


insert into facility values ('100001', 'whale tank');
insert into facility values ('100002', 'shark tank');
insert into facility values ('100003', 'seal beach');
insert into facility values ('100004', 'penguin island');
insert into facility values ('100005', 'dolphin cove');
insert into facility values ('200001', 'seal theater');
insert into facility values ('200002', 'dolphin theater');
insert into facility values ('300001', 'public restroom');

insert into facility_maint values ('100001', '8:00:00', false);
insert into facility_maint values ('100001', '20:00:00', false);
insert into facility_maint values ('100002', '9:00:00', false);
insert into facility_maint values ('100003', '10:00:00', false);
insert into facility_maint values ('100003', '22:00:00', false);
insert into facility_maint values ('100004', '11:00:00', false);
insert into facility_maint values ('100004', '23:00:00', false);
insert into facility_maint values ('100005', '6:00:00', false);
insert into facility_maint values ('100005', '18:00:00', false);
insert into facility_maint values ('200001', '8:00:00', false);
insert into facility_maint values ('200001', '12:00:00', false);
insert into facility_maint values ('200001', '16:00:00', false);
insert into facility_maint values ('200002', '9:00:00', false);
insert into facility_maint values ('200002', '13:00:00', false);
insert into facility_maint values ('200002', '19:00:00', false);
insert into facility_maint values ('300001', '10:00:00', false);
insert into facility_maint values ('300001', '12:00:00', false);
insert into facility_maint values ('300001', '14:00:00', false);
insert into facility_maint values ('300001', '16:00:00', false);
insert into facility_maint values ('300001', '18:00:00', false);

insert into maintain values ('608059001', '100001');
insert into maintain values ('608059001', '100002');
insert into maintain values ('608059001', '100003');
insert into maintain values ('504236312', '100004');
insert into maintain values ('689620370', '100005');
insert into maintain values ('504236312', '200001');
insert into maintain values ('689620370', '200001');
insert into maintain values ('504236312', '200002');
insert into maintain values ('689620370', '200002');
insert into maintain values ('987153744', '300001');

insert into animal values ('101001', 'Marge', 'emperor penguin', 0, '736289249', '100004');
insert into animal values ('101002', 'Homer', 'emperor penguin', 1, '736289249', '100004');
insert into animal values ('102001', 'Bart', 'blue whale', 1, '736289249', '100001');
insert into animal values ('103001', 'Krusty', 'spotted seal', 0, '705628448', '100003');
insert into animal values ('103002', 'Milhouse', 'spotted seal', 1, '705628448', '100003');
insert into animal values ('103003', 'Snowball', 'spotted seal', 1, '705628448', '100003');
insert into animal values ('105001', 'Nibbler', 'bottlenose dolphin', 0, '705628448', '100005');
insert into animal values ('105002', 'Simba', 'bottlenose dolphin', 0, '705628448', '100005');

insert into event values ('101001', 'penguin exhibit', 'exhibit', '100004', '218363685');
insert into event values ('101002', 'whale exhibit', 'exhibit', '100001', '218363685');
insert into event values ('201001', 'seal show', 'performance', '200001', '243910037');
insert into event values ('201002', 'dolphin show', 'performance', '200002', '243910037');

insert into event_instance values ('101001', '2022-05-03', 120);
insert into event_instance values ('101001', '2022-05-04', 130);
insert into event_instance values ('101001', '2022-05-05', null);
insert into event_instance values ('101002', '2022-05-04', 100);
insert into event_instance values ('101002', '2022-05-05', null);
insert into event_instance values ('201001', '2022-05-03', 85);
insert into event_instance values ('201001', '2022-05-04', 93);
insert into event_instance values ('201001', '2022-05-05', null);
insert into event_instance values ('201002', '2022-05-04', 60);
insert into event_instance values ('201002', '2022-05-05', null);

insert into work_on values ('101001', '315400662');
insert into work_on values ('101002', '888748129');
insert into work_on values ('201001', '914191383');
insert into work_on values ('201001', '143705926');
insert into work_on values ('201002', '914191383');
insert into work_on values ('201002', '143705926');

insert into participate values ('101001', '101001');
insert into participate values ('101001', '101002');
insert into participate values ('101002', '102001');
insert into participate values ('201001', '103001');
insert into participate values ('201001', '103002');
insert into participate values ('201002', '105001');
insert into participate values ('201002', '105002');
