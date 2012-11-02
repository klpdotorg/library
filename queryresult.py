def schoolidcheck():
	cur=con.cursor()
	filepointer=csv.writer(open(path+'csv/tocsv/schoolidcheck.csv','w'),delimiter='|',quotechar='\'')
	header=['DEO','BLOCK','KLP SCHOOL ID','SCHOOL NAME']
	cur.execute("select distinct(deo,block,klp_school_id,school_name) from libentry where klp_school_id not in (select id from institution)")
	result=cur.fetchall()
	filepointer.writerow(header)
	for row in result:
		filepointer.writerow(row)
		print row

def booknumcheck():
	cur=con.cursor()
	filepointer=csv.writer(open(path+'csv/tocsv/booknumcheck.csv','w'),delimiter='|',quotechar='\'')
	header=['DEO','ISSUE DATE','BLOCK','KLP SCHOOL ID','SCHOOL NAME','NAME OF THE CHILD','KLP CHILD ID','CLASS','SECTION','AKSHARA BOOK NUMBER','RETURN DATE']
	cur.execute("select * from libentry where akshara_book_number not in (select aksharabooknum from libcopies)")
	result=cur.fetchall()
	filepointer.writerow(header)
	for row in result:
		filepointer.writerow(row)
		print row

schoolidcheck()
