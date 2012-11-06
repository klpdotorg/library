# Database Connection File

import psycopg2

class connection :
        global con;
	con=psycopg2.connect(\
	"dbname='librarycopy' \
	user='postgres' \
	host='localhost' \
	password='qazwsx' \
	");



