
SCRIPT_DIR=`dirname $0`

DBNAME=$(basename $0 .sh)
OWNER=postgres

sudo -u postgres dropdb ${DBNAME}
echo droped db

sudo -u postgres createdb -E UTF8 ${DBNAME}
echo created db

sudo -u ${OWNER} createlang plpgsql ${DBNAME}
echo created language

sudo -u postgres psql -d ${DBNAME} -f /usr/share/postgresql/8.4/contrib/dblink.sql
echo loaded functions

#echo creating dblink
#sudo -u postgres psql -d ${DBNAME} -c "CREATE EXTENSION dblink"

# Create schema
echo creating schema
psql -U ${OWNER} -d ${DBNAME} -f ${SCRIPT_DIR}/${DBNAME}.sql

echo "Reading csv Files writing to load.sql file"
# Writing to .sql file
python ${SCRIPT_DIR}/${DBNAME}.py

#loading data to database
sudo -u ${OWNER} psql -d ${DBNAME} -f ${SCRIPT_DIR}/load.sql

#Searching result
python ${SCRIPT_DIR}/queryresult.py






