#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Array of realm specifications.
declare -a _REALM_SPECIALIZATIONS=(
	'aerosols'
	'atmos'
	'atmospheric-chemistry'
	'landice'
	'landsurface'
	'ocean'
	'ocnbgchem'
	'seaice'
)

# Array of active (i.e. valid) specifications.
declare -a _ACTIVE_SPECIALIZATIONS=(
	'toplevel'
	'atmos'
	'ocean'
	'ocnbgchem'
	'seaice'
)

# Sync CIM profile.
_sync_cim_profile()
{
	log "PYESDOC : syncing cmip6 specialization CIM profile ..."

	for specialization in "${_REALM_SPECIALIZATIONS[@]}"
	do
		cp $ESDOC_DIR_REPOS/cmip6-specializations-toplevel/cim_profile.py $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/generate/cim_profile.py
	done

	log "PYESDOC : ... synced"
}

# Sync python definitions.
_sync_definitions()
{
	log "PYESDOC : syncing cmip6 specialization definitions ..."

	for specialization in "${_ACTIVE_SPECIALIZATIONS[@]}"
	do
		# ... switch output file names.
		declare file_prefix=$specialization

		# ... Update pyesdoc.
		rm $ESDOC_DIR_REPOS/esdoc-py-client/pyesdoc/mp/specializations/cmip6/$file_prefix*.py
		cp $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/$file_prefix*.py $ESDOC_DIR_REPOS/esdoc-py-client/pyesdoc/mp/specializations/cmip6

		# ... update generated artefacts.
		python $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/generate --type=mm
		python $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/generate --type=json
		python $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/generate --type=ids-level-1
		python $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/generate --type=ids-level-2
		python $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/generate --type=ids-level-3

		# ... remove previously generated docs
		rm $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/config/$file_prefix.json
		rm $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/csv/$file_prefix*.csv
		rm $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/mindmaps/$file_prefix.mm
		# ... copy generated docs
		cp $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/_$file_prefix.mm $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/mindmaps/$file_prefix.mm
		cp $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/_$file_prefix.json $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/config/$file_prefix.json
		cp $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/_$file_prefix-ids-level-1.csv $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/csv/$file_prefix-ids-level-1.csv
		cp $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/_$file_prefix-ids-level-2.csv $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/csv/$file_prefix-ids-level-2.csv
		cp $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/_$file_prefix-ids-level-3.csv $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/csv/$file_prefix-ids-level-3.csv

	done

	log "PYESDOC : ... synced"
}

# Sync templates.
_sync_templates()
{
	log "PYESDOC : syncing cmip6 specialization templates ..."

	for specialization in "${_REALM_SPECIALIZATIONS[@]}"
	do
		# ... remove previous
		rm -rf $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/templates
		mkdir $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/templates
		# ... copy current
		cp $ESDOC_DIR_REPOS/cmip6-specializations-toplevel/templates/* $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/templates
	done

	log "PYESDOC : ... synced"
}

# Main entry point.
main()
{
	source $ESDOC_HOME/bash/cmip6/specializations/sync_tooling.sh
	_sync_templates
	_sync_cim_profile
	_sync_definitions
}

# Invoke entry point.
main
