#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Main entry point.
main()
{
	log "PYESDOC : syncing cmip6 specialization tooling ..."

	# Set of specializations.
	declare -a SPECIALIZATIONS=(
		'aerosols'
		'atmos'
		'atmospheric-chemistry'
		'landice'
		'landsurface'
		'ocean'
		'ocnbgchem'
		'seaice'
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
		cp $ESDOC_DIR_REPOS/cmip6-specializations-toplevel/generate/* $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/generate
		cp $ESDOC_DIR_REPOS/cmip6-specializations-toplevel/validate/* $ESDOC_DIR_REPOS/cmip6-specializations-$specialization/validate
		log "PYESDOC : ... synced: "$specialization
	done

	# Sync to pyesdoc.
	cp $ESDOC_DIR_REPOS/cmip6-specializations-toplevel/generate/utils_constants.py $ESDOC_DIR_REPOS/esdoc-py-client/pyesdoc/mp/specializations
	cp $ESDOC_DIR_REPOS/cmip6-specializations-toplevel/generate/utils_factory.py $ESDOC_DIR_REPOS/esdoc-py-client/pyesdoc/mp/specializations
	cp $ESDOC_DIR_REPOS/cmip6-specializations-toplevel/generate/utils_loader.py $ESDOC_DIR_REPOS/esdoc-py-client/pyesdoc/mp/specializations
	cp $ESDOC_DIR_REPOS/cmip6-specializations-toplevel/generate/utils_model.py $ESDOC_DIR_REPOS/esdoc-py-client/pyesdoc/mp/specializations
	cp $ESDOC_DIR_REPOS/cmip6-specializations-toplevel/generate/utils_parser.py $ESDOC_DIR_REPOS/esdoc-py-client/pyesdoc/mp/specializations
}

# Invoke entry point.
main
