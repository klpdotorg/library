DROP TABLE IF EXISTS "level_agg" cascade;
create table level_agg (
	klp_school_id integer, 
	class integer, 
	month varchar(10), 
	year varchar(10), 
	book_level varchar(50), 
	child_count integer
	);

DROP TABLE IF EXISTS "lang_agg" cascade;
create table lang_agg (
	klp_school_id integer, 
	class integer, 
	month varchar(10), 
	year varchar(10), 
	book_lang varchar(50), 
	child_count integer
	);

insert into level_agg select a.klp_school_id,a.class,split_part(a.issue_date,'/',2) as month, split_part(a.issue_date,'/',3) as year,b.booklevel as book_level,count(klp_child_id) as child_count from vw_correctbooknumbers as a,vw_libtitles as b,language as l,vw_libcopies as c where substr(a.akshara_book_number,1,3)=l.id and l.name=b.language and cast(substr(a.akshara_book_number,4,6) as int)=cast(b.titleno as int) and c.aksharabooknum=a.akshara_book_number and c.titleid=b.titleid group by klp_school_id,class,month,year,book_level;

insert into lang_agg select a.klp_school_id,a.class,split_part(a.issue_date,'/',2) as month, split_part(a.issue_date,'/',3) as year,b.language as book_lang,count(klp_child_id) as child_count from vw_correctbooknumbers as a,vw_libtitles as b,language as l,vw_libcopies as c where substr(a.akshara_book_number,1,3)=l.id and l.name=b.language and cast(substr(a.akshara_book_number,4,6) as int)=cast(b.titleno as int) and c.aksharabooknum=a.akshara_book_number and c.titleid=b.titleid group by klp_school_id,class,month,year,book_lang;
