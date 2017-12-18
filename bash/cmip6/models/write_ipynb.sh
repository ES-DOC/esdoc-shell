#!/bin/bash

# Import utils.
source $ESDOC_HOME/bash/utils.sh

# Main entry point.
main()
{
	log "CMIP6 model notebooks writing begins ..."

	activate_venv
	python $ESDOC_HOME/bash/cmip6/models/write_ipynb --institute=$1

	log "CMIP6 model notebooks written ..."
}

# Invoke entry point.
main $1
