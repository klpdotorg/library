

DROP TABLE IF EXISTS "libentry" cascade;
create table libentry (
	deo varchar(15), 
	issue_date varchar(20), 
	block varchar(50), 
	klp_school_id numeric(7,0), 
	school_name varchar(50), 
	name_of_the_child char(25), 
	klp_child_id varchar(30), 
	class numeric(3,0), 
	section varchar(8), 
	akshara_book_number varchar(50), 
	return_date varchar(20)
	);

DROP TABLE IF EXISTS "language" cascade;
create table language(
	id varchar(4),
	name varchar(50)
	);

insert into language values('EH0','E/H');
insert into language values('EK0','E/K');
insert into language values('E00','ENGLISH');
insert into language values('H00','HINDI');
insert into language values('K00','KANNADA');
insert into language values('TA0','TAMIL');
insert into language values('TE0','TELUGU');
insert into language values('U00','URDU');

CREATE OR REPLACE VIEW vw_institution as
       select * from dblink('host=localhost dbname=klp_institution_master user=postgres password=qazwsx', 'select id from schools_institution')
       as t1 (id integer
	);

CREATE OR REPLACE VIEW vw_libcopies as
       select * from dblink('host=localhost dbname=klplibmaster user=postgres password=qazwsx', 'select titleid,aksharabooknum from tb_libcopies')
       as t1 (titleid integer,
	aksharabooknum character varying(50)
	);

CREATE OR REPLACE VIEW vw_libtitles as
       select * from dblink('host=localhost dbname=klplibmaster user=postgres password=qazwsx', 'select * from tb_libtitles')
       as t1 (titleid integer,
	titleno character varying(50),
	language character varying(50),
	publisher character varying(100),
	agegroup character varying(100),
	titlename character varying(500),
	booklevel character varying(50)
	);

create or replace view vw_booknumbers as 
	select distinct(akshara_book_number) from libentry where ((length(akshara_book_number)>9 and length(akshara_book_number)<=15) and akshara_book_number not in(select distinct(titlename) from vw_libtitles where titlename in(select distinct(akshara_book_number) from libentry)));

create or replace view vw_correctbooknumbers as 
	select *from libentry where akshara_book_number in(select * from vw_booknumbers where akshara_book_number in (select aksharabooknum from vw_libcopies));
