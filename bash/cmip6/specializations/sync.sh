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
		'atmosphere'
		'ocean'
		'oceanbgc'
		'seaice'
	)

	# Update pyesdoc.
	for specialization in "${SPECIALIZATIONS[@]}"
	do
		rm $ESDOC_DIR_REPOS/esdoc-py-client/pyesdoc/mp/specializations/cmip6/$specialization*.py
		cp $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/$specialization*.py $ESDOC_DIR_REPOS/esdoc-py-client/pyesdoc/mp/specializations/cmip6
	done

	# Update generated artefacts.
	for specialization in "${SPECIALIZATIONS[@]}"
	do
		python $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/generate --type=mm
		python $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/generate --type=json
		python $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/generate --type=ids-level-1
		python $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/generate --type=ids-level-2
		python $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/generate --type=ids-level-3
	done

	# Updated esdoc-docs.
	for specialization in "${SPECIALIZATIONS[@]}"
	do
		# ... remove previously generated
		rm $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/config/$specialization.json
		rm $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/csv/$specialization*.csv
		rm $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/mindmaps/$specialization.mm
		# ... copy generated
		cp $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/_$specialization.mm $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/mindmaps/$specialization.mm
		cp $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/_$specialization.json $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/config/$specialization.json
		cp $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/_$specialization-ids-level-1.csv $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/csv/$specialization-ids-level-1.csv
		cp $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/_$specialization-ids-level-2.csv $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/csv/$specialization-ids-level-2.csv
		cp $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/_$specialization-ids-level-3.csv $ESDOC_DIR_REPOS/esdoc-docs/cmip6/models/csv/$specialization-ids-level-3.csv
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

# Sync tooling.
_sync_tooling()
{
	log "PYESDOC : syncing cmip6 specialization tooling ..."

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
		rm -rf $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/generate
		mkdir $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/generate
		rm -rf $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/validate
		mkdir $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/validate
		# ... copy current
		cp $ESDOC_DIR_REPOS/cmip6-specializations-ocean/generate/* $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/generate
		cp $ESDOC_DIR_REPOS/cmip6-specializations-ocean/validate/* $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/validate
	done

	# Sync to pyesdoc.
	cp $ESDOC_DIR_REPOS/cmip6-specializations-ocean/generate/utils_factory.py $ESDOC_DIR_REPOS/esdoc-py-client/pyesdoc/mp/specializations
	cp $ESDOC_DIR_REPOS/cmip6-specializations-ocean/generate/utils_loader.py $ESDOC_DIR_REPOS/esdoc-py-client/pyesdoc/mp/specializations
	cp $ESDOC_DIR_REPOS/cmip6-specializations-ocean/generate/utils_model.py $ESDOC_DIR_REPOS/esdoc-py-client/pyesdoc/mp/specializations
	cp $ESDOC_DIR_REPOS/cmip6-specializations-ocean/generate/utils_parser.py $ESDOC_DIR_REPOS/esdoc-py-client/pyesdoc/mp/specializations
}

# Main entry point.
main()
{
	_sync_cim_profile
	_sync_definitions
	_sync_templates
	_sync_tooling
}

# Invoke entry point.
main
