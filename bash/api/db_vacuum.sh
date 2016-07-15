source $ESDOC_HOME/bash/init.sh

log "DB : vacuuming postgres db ..."

psql -U esdoc_db_admin -d esdoc_api -q -f $ESDOC_HOME/bash/api/db_vacuum.sql

log "DB : vacuumed postgres db"
