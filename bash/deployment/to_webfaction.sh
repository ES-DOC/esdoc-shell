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
	    	echo -e "ES-DOC DEPLOYMENT > "$tabs$1
	    else
	    	echo -e "ES-DOC DEPLOYMENT > "$1
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
# Update libs
# -------------------------------------------------------------------------------
# ... archive
_log_banner
_log "updating document archive ..."
_log_banner

cd $HOME/weblibs/$1/esdoc-archive
git pull
source ./sh/activate
esdoc-archive-uncompress
_log_end

# ... pyesdoc
_log_banner
_log "updating pyesdoc lib ..."
_log_banner

cd $HOME/weblibs/$1/esdoc-py-client
git pull
source ./sh/activate
_log_end

# -------------------------------------------------------------------------------
# Update front-ends
# -------------------------------------------------------------------------------

declare -a _ESDOC_FRONT_ENDS=(
	'compare'
	'demo'
	'errata'
	'search'
	'splash'
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

# Update errata index.html.
cp $HOME/webapps/$1_fe_errata/search.html $HOME/webapps/$1_fe_errata/index.html

# -------------------------------------------------------------------------------
# Update web-services
# -------------------------------------------------------------------------------
declare -a _ESDOC_WEB_SERVICES=(
	'cdf2cim'
	'documentation'
	'errata'
	'url_rewriter_doc'
	'url_rewriter_fi'
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

# Reload daemons.
# ... cdf2cim
_log_banner
_log "reloading web-service: "$1_ws_cdf2cim
_log_banner

source $HOME/webapps/$1_ws_cdf2cim/sh/activate
cdf2cim-ws-daemon-reload
_log_end

# ... documentation
_log_banner
_log "reloading web-service: "$1_ws_documentation
_log_banner

source $HOME/webapps/$1_ws_documentation/sh/activate
esdoc-ws-daemon-reload
_log_end

# ... errata
_log_banner
_log "reloading web-service: "$1_ws_errata
_log_banner

source $HOME/webapps/$1_ws_errata/sh/activate
errata-ws-daemon-reload
_log_end

# ... url rewriter (doc)
_log_banner
_log "reloading web-service: "$1_ws_url_rewriter_doc
_log_banner

source $HOME/webapps/$1_ws_url_rewriter_doc/sh/activate
rewriter-ws-daemon-reload
_log_end

# ... url rewriter (further info)
_log_banner
_log "reloading web-service: "$1_ws_url_rewriter_fi
_log_banner

source $HOME/webapps/$1_ws_url_rewriter_fi/sh/activate
rewriter-ws-daemon-reload
_log_end

# -------------------------------------------------------------------------------
# Finalization
# -------------------------------------------------------------------------------
_log_banner
_log $1" deployment complete"
_log_banner
_log_end