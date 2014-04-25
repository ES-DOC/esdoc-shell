# ###############################################################
# SECTION: DB FUNCTIONS
# ###############################################################

# Drop db.
_db_restore()
{
	log "... restoring DB"

	unzip -q $DIR_DB/backups/db.zip -d $DIR_TMP
	pg_restore -U postgres -d esdoc_api $DIR_TMP/db
	pg_restore -U postgres -d esdoc_api_test $DIR_TMP/db
	reset_tmp
}

# Drop db.
_db_drop()
{
	log "... dropping DB"

	dropdb -U postgres esdoc_api --if-exists
	dropdb -U postgres esdoc_api_test --if-exists
}

# Create db.
_db_create()
{
	log "... creating DB"

	createdb -U postgres -e -O postgres -T template0 esdoc_api
	createdb -U postgres -e -O postgres -T template0 esdoc_api_test
}

# Seed db.
_db_seed()
{
	log "DB: seeding ..."

	activate_venv api
	python ./exec.py "db-setup"
}

# Backup db.
run_db_backup()
{
	log "TODO : DB back up ..."
}

# Install db.
run_db_install()
{
	log "DB : installing ..."

	_db_create
	_db_seed

	log "DB : installed ..."
}

# Reset db.
run_db_reset()
{
	log "DB : resetting ..."

	run_db_uninstall
	run_db_install

	log "DB : reset"
}

# Setup db.
run_db_setup()
{
	log "DB: initializing ..."

	_db_drop
	_db_create
	_db_seed

	log "TODO - seed test db"

	log "DB: initialized"
}

# Launches api db ingestion job.
run_db_ingest()
{
    log "DB: ingesting from external sources ..."

	activate_venv api
	python ./exec.py "db-ingest"
}

# Restores api db from deplyoyment backup file.
run_db_restore()
{
    log "DB: restoring ..."

	_db_drop
	_db_create
	_db_restore

    log "DB: restored"
}

# Uninstall db.
run_db_uninstall()
{
	log "DB : uninstalling ..."

	run_db_backup
	_db_drop

	log "DB : uninstalled"
}
