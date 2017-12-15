#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Main entry point.
main()
{
	log "CMIP6 model notebooks writing begins ..."

	activate_venv
	rm -r $ESDOC_DIR_REPOS/esdoc-jupyterhub/notebooks
	python $ESDOC_HOME/bash/cmip6/models/write_notebooks

	log "CMIP6 model notebooks written ..."
}

# Invoke entry point.
main
