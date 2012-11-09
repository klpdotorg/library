
SCRIPT_DIR=`dirname $0`

DBNAME=$(basename $0 .sh)
OWNER=postgres

#sudo -u ${OWNER} dropdb ${DBNAME}
echo droped db

#sudo -u ${OWNER} createdb -E UTF8 ${DBNAME}
echo created db

#sudo -u ${OWNER} createlang plpgsql ${DBNAME}
echo created language

#sudo -u ${OWNER} psql -d ${DBNAME} -f /usr/share/postgresql/8.4/contrib/dblink.sql
echo loaded functions

#echo creating dblink
#sudo -u postgres psql -d ${DBNAME} -c "CREATE EXTENSION dblink"

# Create schema
echo creating schema
#sudo -u postgres psql -U ${OWNER} -d ${DBNAME} -f ${SCRIPT_DIR}/${DBNAME}.sql

echo creating connection to postgres
#python ${SCRIPT_DIR}/connection.py

echo "Reading csv Files writing to load.sql file"
# Writing to .sql file
#python ${SCRIPT_DIR}/${DBNAME}.py

#loading data to database
#sudo -u ${OWNER} psql -d ${DBNAME} -f ${SCRIPT_DIR}/load.sql

echo Writing result
#python ${SCRIPT_DIR}/queryresult.py

echo aggregate functions
sudo -u ${OWNER} psql -d ${DBNAME} -f ${SCRIPT_DIR}/Agg.sql


