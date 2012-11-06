

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

CREATE OR REPLACE VIEW vw_institution as
       select * from dblink('host=localhost dbname=klp_institution_master user=postgres password=qazwsx', 'select id from schools_institution')
       as t1 (id integer
	);

CREATE OR REPLACE VIEW vw_libcopies as
       select * from dblink('host=localhost dbname=klplibmaster user=postgres password=qazwsx', 'select aksharabooknum from tb_libcopies')
       as t1 (aksharabooknum character varying(50)
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
