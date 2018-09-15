#!/bin/bash

# Import utils.
source $ESDOC_DIR_BASH/utils.sh

# Import vocab.
source $ESDOC_DIR_BASH/cmip6/specializations/vocab.sh

# Main entry point.
main()
{
	log "CMIP6-SPECS : syncing tooling ..."

	# Sync definitions.
	for specialization in "${CMIP6_REALM_SPECIALIZATIONS[@]}"
	do
		# ... generator
		rm -rf $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization/generate
		mkdir $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization/generate
		cp -r $ESDOC_DIR_CMIP6/cmip6-specializations-toplevel/generate/* $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization/generate

		# ... validator
		rm -rf $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization/validate
		mkdir $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization/validate
		cp -r $ESDOC_DIR_CMIP6/cmip6-specializations-toplevel/validate/* $ESDOC_DIR_CMIP6/cmip6-specializations-$specialization/validate

		log "CMIP6-SPECS : ... synced: "$specialization
	done

	# Sync to pyesdoc.
	cp $ESDOC_DIR_CMIP6/cmip6-specializations-toplevel/generate/utils.py $ESDOC_DIR_REPOS_CORE/esdoc-py-client/pyesdoc/mp/specializations
	cp $ESDOC_DIR_CMIP6/cmip6-specializations-toplevel/generate/utils_cache.py $ESDOC_DIR_REPOS_CORE/esdoc-py-client/pyesdoc/mp/specializations
	cp $ESDOC_DIR_CMIP6/cmip6-specializations-toplevel/generate/utils_constants.py $ESDOC_DIR_REPOS_CORE/esdoc-py-client/pyesdoc/mp/specializations
	cp $ESDOC_DIR_CMIP6/cmip6-specializations-toplevel/generate/utils_factory.py $ESDOC_DIR_REPOS_CORE/esdoc-py-client/pyesdoc/mp/specializations
	cp $ESDOC_DIR_CMIP6/cmip6-specializations-toplevel/generate/utils_loader.py $ESDOC_DIR_REPOS_CORE/esdoc-py-client/pyesdoc/mp/specializations
	cp $ESDOC_DIR_CMIP6/cmip6-specializations-toplevel/generate/utils_model.py $ESDOC_DIR_REPOS_CORE/esdoc-py-client/pyesdoc/mp/specializations
	cp $ESDOC_DIR_CMIP6/cmip6-specializations-toplevel/generate/utils_parser.py $ESDOC_DIR_REPOS_CORE/esdoc-py-client/pyesdoc/mp/specializations
	log "CMIP6-SPECS : ... synced: pyesdoc"

	log "CMIP6-SPECS : synced tooling"
}

# Invoke entry point.
main
