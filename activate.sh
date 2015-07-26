# Set paths.
DIR_ESDOC_HOME="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DIR_ESDOC_PYESDOC=$DIR_ESDOC_HOME/repos/esdoc-py-client
DIR_ESDOC_API=$DIR_ESDOC_HOME/repos/esdoc-api
DIR_ESDOC_STATIC=$DIR_ESDOC_HOME/repos/esdoc-static

# Root alias.
alias esdoc=$DIR_ESDOC_HOME'/exec.sh'

# API commands.
alias esdoc-api='esdoc api'
alias esdoc-api-db-index='esdoc api-db-index'
alias esdoc-api-db-index-reset='esdoc api-db-index-reset'
alias esdoc-api-db-ingest='esdoc api-db-ingest'
alias esdoc-api-db-install='esdoc api-db-install'
alias esdoc-api-db-reset='esdoc api-db-reset'
alias esdoc-api-db-uninstall='esdoc api-db-uninstall'
alias esdoc-api-db-insert-project='esdoc api-db-insert-project'
alias esdoc-api-db-write-stats='python '$DIR_ESDOC_API'/jobs/run_write_stats.py --outdir='$DIR_ESDOC_STATIC'/data'

# Archive commands.
alias esdoc-archive-compress='esdoc archive-compress'
alias esdoc-archive-echo='esdoc archive-echo'
alias esdoc-archive-populate='esdoc archive-populate'
alias esdoc-archive-uncompress='esdoc archive-uncompress'

# Document commands.
alias esdoc-doc-validate='esdoc doc-validate'
alias esdoc-doc-convert='esdoc doc-convert'

# Meta-programming commands.
alias esdoc-mp='esdoc mp'

# Stack commands.
alias esdoc-stack-bootstrap='esdoc stack-bootstrap'
alias esdoc-stack-install='esdoc stack-install'
alias esdoc-stack-update='esdoc stack-update'
alias esdoc-stack-update-shell='esdoc stack-update-shell'
alias esdoc-stack-update-repo='esdoc stack-update-repo'
alias esdoc-stack-update-repos='esdoc stack-update-repos'
alias esdoc-stack-update-venv='esdoc stack-update-venv'
alias esdoc-stack-update-venvs='esdoc stack-update-venvs'
alias esdoc-stack-uninstall='esdoc stack-uninstall'

# Help commands.
alias esdoc-help='esdoc help'

# Deployment commands.
alias esdoc-shells-view='ps -ef | grep esdoc/shells'
alias esdoc-deploy=$DIR_ESDOC_HOME'/ops/venv/python/bin/python '$DIR_ESDOC_HOME'/deploy.py'

# Misc commands.
alias esdoc-pyesdoc-tests='esdoc pyesdoc-tests'
alias esdoc-js-plugin-compile='esdoc js-plugin-compile'

# Unset variables
unset DIR_ESDOC_HOME
unset DIR_ESDOC_PYESDOC
unset DIR_ESDOC_API
unset DIR_ESDOC_STATIC
