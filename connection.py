# Database Connection File

import psycopg2

class connection :
        global con;
	con=psycopg2.connect(\
	"dbname='library' \
	user='postgres' \
	host='localhost' \
	password='qazwsx' \
	");



