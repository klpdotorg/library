# Library Assignment

from connection import *
import csv
import re

path='/home/jagadeesh/klp/library/libentrydata/'

def schoolidcheck():
	print "Started School id check"
	cur=con.cursor()
	filepointer=csv.writer(open(path+'csv/tocsv/schoolidcheck.csv','w'),delimiter='|',quotechar='\'')
	header=['DEO','BLOCK','KLP SCHOOL ID','SCHOOL NAME']
	cur.execute("select distinct(deo,block,klp_school_id,school_name) from libentry where klp_school_id not in (select id from vw_institution)")
	result=cur.fetchall()
	filepointer.writerow(header)
	for row in result:
		filepointer.writerow(row)
#		print row
	print "School id check copleted"

def titlesfound():
	print "Started titles checking"
	cur=con.cursor()
	filepointer=csv.writer(open(path+'csv/tocsv/titlesfound.csv','w'),delimiter='|',quotechar='\'')
	header=['DEO','ISSUE DATE','BLOCK','KLP SCHOOL ID','SCHOOL NAME','NAME OF THE CHILD','KLP CHILD ID','CLASS','SECTION','AKSHARA BOOK NUMBER','RETURN DATE']
	cur.execute("select * from libentry where akshara_book_number in (select distinct(titlename) from vw_libtitles where titlename in(select distinct(akshara_book_number) from libentry))")
	result=cur.fetchall()
	filepointer.writerow(header)
	for row in result:
		filepointer.writerow(row)
#		print row
	print "Titles check copleted"

def book_no_len_less_than_10():
	print "Checking for booknumbers length is less"
	cur=con.cursor()
	filepointer=csv.writer(open(path+'csv/tocsv/lenless10.csv','w'),delimiter='|',quotechar='\'')
	header=['DEO','ISSUE DATE','BLOCK','KLP SCHOOL ID','SCHOOL NAME','NAME OF THE CHILD','KLP CHILD ID','CLASS','SECTION','AKSHARA BOOK NUMBER','RETURN DATE']
	cur.execute("select * from libentry where length(akshara_book_number)<=9 and akshara_book_number not in(select distinct(titlename) from vw_libtitles where titlename in(select distinct(akshara_book_number) from libentry))")
	result=cur.fetchall()
	filepointer.writerow(header)
	for row in result:
		filepointer.writerow(row)
#		print row
	print "booknumbers length is less completed"

def book_no_len_gr_than_15():
	print "Checking booknumbers length is greater than 15"
	cur=con.cursor()
	filepointer=csv.writer(open(path+'csv/tocsv/lengr15.csv','w'),delimiter='|',quotechar='\'')
	header=['DEO','ISSUE DATE','BLOCK','KLP SCHOOL ID','SCHOOL NAME','NAME OF THE CHILD','KLP CHILD ID','CLASS','SECTION','AKSHARA BOOK NUMBER','RETURN DATE']
	cur.execute("select * from libentry where length(akshara_book_number)>15 and akshara_book_number not in(select distinct(titlename) from vw_libtitles where titlename in(select distinct(akshara_book_number) from libentry))")
	result=cur.fetchall()
	filepointer.writerow(header)
	for row in result:
		filepointer.writerow(row)
#		print row
	print "Checking booknumbers length is greater than 15 copmleted"

def create_view_for_booknumbers():
	cur=con.cursor()
	cur.execute("create or replace view vw_booknumbers as select distinct(akshara_book_number) from libentry where ((length(akshara_book_number)>9 and length(akshara_book_number)<=15) and akshara_book_number not in(select distinct(titlename) from vw_libtitles where titlename in(select distinct(akshara_book_number) from libentry)))")

def book_number_check():
	print "Checcking booknumbers against libcopies"
	cur=con.cursor()
	filepointer=csv.writer(open(path+'csv/tocsv/booknumcheck.csv','w'),delimiter='|',quotechar='\'')
	header=['DEO','ISSUE DATE','BLOCK','KLP SCHOOL ID','SCHOOL NAME','NAME OF THE CHILD','KLP CHILD ID','CLASS','SECTION','AKSHARA BOOK NUMBER','RETURN DATE']
	cur.execute("select *from libentry where akshara_book_number in(select * from vw_booknumbers where akshara_book_number not in (select aksharabooknum from vw_libcopies))")
	result=cur.fetchall()
	filepointer.writerow(header)
	for row in result:
		filepointer.writerow(row)
#		print row
	print "Checking booknumbers against libcopies completed" 
	
schoolidcheck()
titlesfound()
book_no_len_less_than_10()
book_no_len_gr_than_15()
create_view_for_booknumbers()
book_number_check()

