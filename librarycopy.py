# Library Assignment

from connection import *
import os
import glob
import csv
import re

path='/home/jagadeesh/klp/library/libentrydata/'

def rm_spc_char(value):
	text=''
	for c in value:
		if c!='\'' and c!='\\' and c!='`':
			text=text+c
	return text

def chk_name(value):
	if (value if isinstance(value,str) else '')=='':
		return 'blank'
	else:
		return value

def split_cls(value,rel):
	if rel==1:
		if value:
			try:
				s=int(value[0])
				return str(s)
			except:
				return 'NULL'
		else:
			return 'NULL'
	elif rel==2:
		if value:
			prv=''
			for ch in value:
				c=ch.upper()
				if c=='A' or c=='B' or c=='C' or c=='D':
					if prv!='R' and prv!='N':
						return c
				prv=c
			return ''
		else:
			return ''

def chk_null(value):
	if value:
		return value
	else:
		return 'NULL'

def copytoloadfile():
	filepointer1=open('/home/jagadeesh/klp/library/load.sql','w')
	for files in glob.glob(os.path.join(path+'csv/','*.*')):
		print files
		filepointer=csv.reader(open(files,'r'),delimiter='|',quotechar='\'')
		i=0
		filepointer.next()
		for row in filepointer:
			filepointer1.write("insert into libentry values('"+chk_name(row[0]).lower().strip()+"','"+row[1].replace(' ','')+"','"+row[2].strip()+"',"+chk_null(row[3])+",'"+rm_spc_char(row[4]).strip()+"','"+rm_spc_char(row[5]).strip()+"','"+row[6].strip()+"',"+split_cls(rm_spc_char(row[7].replace(' ','')),1)+",'"+split_cls(rm_spc_char(row[7].replace(' ','')),2)+"','"+rm_spc_char(row[8]).strip()+"','"+(row[9]+"/"+row[10]+"/"+row[11]).replace(' ','')+"');\n")
			
			i=i+1
		print i
	filepointer1.close()


copytoloadfile()


