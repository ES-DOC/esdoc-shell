#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh


# Sync CIM profile.
_sync_cim_profile()
{
	log "PYESDOC : syncing cmip6 specialization CIM profile ..."

	# Set of specializations.
	declare -a SPECIALIZATIONS=(
		'aerosols'
		'atmosphere'
		'atmospheric-chemistry'
		'landice'
		'landsurface'
		'oceanbgc'
		'seaice'
		'toplevel'
	)

	# Sync definitions.
	for specialization in "${SPECIALIZATIONS[@]}"
	do
		cp $ESDOC_DIR_REPOS/cmip6-specializations-toplevel/cim_profile.py $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/generate/cim_profile.py
	done
}

# Sync python definitions.
_sync_definitions()
{
	log "PYESDOC : syncing cmip6 specialization definitions ..."

	# Set of specializations.
	declare -a SPECIALIZATIONS=(
		'toplevel'
		'atmosphere'
		'ocean'
		'oceanbgc'
		'seaice'
	)

	# Update pyesdoc.
	for specialization in "${SPECIALIZATIONS[@]}"
	do
		if [ $specialization = "toplevel" ]; then
			declare file_prefix="model"
		else
			declare file_prefix=$specialization
		fi

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
}

# Sync templates.
_sync_templates()
{
	log "PYESDOC : syncing cmip6 specialization templates ..."

	# Set of specializations.
	declare -a SPECIALIZATIONS=(
		'aerosols'
		'atmosphere'
		'atmospheric-chemistry'
		'landice'
		'landsurface'
		'oceanbgc'
		'seaice'
		'toplevel'
	)

	# Sync definitions.
	for specialization in "${SPECIALIZATIONS[@]}"
	do
		# ... remove previous
		rm -rf $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/templates
		mkdir $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/templates
		# ... copy current
		cp $ESDOC_DIR_REPOS/cmip6-specializations-ocean/templates/* $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/templates
	done
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
