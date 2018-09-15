# Wraps standard echo by adding ESDOC prefix.
_log()
{
	declare tabs=''
	if [ "$1" ]; then
		if [ "$2" ]; then
			for ((i=0; i<$2; i++))
			do
				declare tabs+='\t'
			done
	    	echo -e "ESDOC-DEPLOYMENT > "$tabs$1
	    else
	    	echo -e "ESDOC-DEPLOYMENT > "$1
	    fi
	else
	    echo -e ""
	fi
}

_log_banner()
{
	echo "----------------------------------------------------------------"
}

_log_end()
{
	echo ""
}

# -------------------------------------------------------------------------------
# Update archive
# -------------------------------------------------------------------------------
_log_banner
_log "updating document archive ..."
_log_banner
cd $HOME/weblibs/esdoc-archive
git pull
source ./sh/activate
esdoc-archive-uncompress
_log_end

# -------------------------------------------------------------------------------
# Update libs
# -------------------------------------------------------------------------------

# pyesdoc
_log_banner
_log "updating pyesdoc lib ..."
_log_banner
cd $HOME/weblibs/esdoc-py-client
git pull
source ./sh/activate
_log_end

# pyessv
_log_banner
_log "updating pyessv lib ..."
_log_banner
cd $HOME/weblibs/pyessv
git pull
source ./sh/activate
_log_end

# pyessv-archive
_log_banner
_log "updating pyessv-archive ..."
_log_banner
cd $HOME/weblibs/pyessv-archive
git pull
source ./sh/activate
_log_end

# docs
_log_banner
_log "updating docs ..."
_log_banner
cd $HOME/weblibs/esdoc-docs
git pull
_log_end

# -------------------------------------------------------------------------------
# Update front-ends
# -------------------------------------------------------------------------------

declare -a _ESDOC_FRONT_ENDS=(
	'compare'
	'demo'
	'search'
	'specializations'
	'static'
	'view'
)

# Simply pull latest from GH.
for _ESDOC_FRONT_END in "${_ESDOC_FRONT_ENDS[@]}"
do
	_log_banner
	_log "updating front-end: "$1_fe_$_ESDOC_FRONT_END
	_log_banner
	cd $HOME/webapps/$1_fe_$_ESDOC_FRONT_END
	git pull
	_log_end
done

# -------------------------------------------------------------------------------
# Update web-services
# -------------------------------------------------------------------------------
declare -a _ESDOC_WEB_SERVICES=(
	'cdf2cim'
	'documentation'
	'url_rewriter_doc'
	'url_rewriter_fi'
	'url_rewriter_specs'
)

# Simply pull latest from GH.
for _ESDOC_WEB_SERVICE in "${_ESDOC_WEB_SERVICES[@]}"
do
	_log_banner
	_log "updating web-service: "$1_ws_$_ESDOC_WEB_SERVICE
	_log_banner
	cd $HOME/webapps/$1_ws_$_ESDOC_WEB_SERVICE
	git pull
	_log_end
done

# Reload cdf2cim daemon
_log_banner
_log "reloading web-service: "$1_ws_cdf2cim
_log_banner
source $HOME/webapps/$1_ws_cdf2cim/sh/activate
cdf2cim-ws-daemon-reload
_log_end

# Reload documentation daemon
_log_banner
_log "reloading web-service: "$1_ws_documentation
_log_banner
source $HOME/webapps/$1_ws_documentation/sh/activate
esdoc-ws-daemon-reload
_log_end

# Reload url rewriter (doc) daemon
_log_banner
_log "reloading web-service: "$1_ws_url_rewriter_doc
_log_banner
source $HOME/webapps/$1_ws_url_rewriter_doc/sh/activate
rewriter-ws-daemon-reload
_log_end

# Reload url rewriter (further info) daemon
_log_banner
_log "reloading web-service: "$1_ws_url_rewriter_fi
_log_banner
source $HOME/webapps/$1_ws_url_rewriter_fi/sh/activate
rewriter-ws-daemon-reload
_log_end

# Reload url rewriter (specs) daemon
_log_banner
_log "reloading web-service: "$1_ws_url_rewriter_specs
_log_banner
source $HOME/webapps/$1_ws_url_rewriter_specs/sh/activate
rewriter-ws-daemon-reload
_log_end

# -------------------------------------------------------------------------------
# Finalization
# -------------------------------------------------------------------------------
cd $HOME
_log_banner
_log $1" deployment complete"
_log_banner
_log_end
