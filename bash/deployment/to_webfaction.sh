# -------------------------------------------------------------------------------
# Update libs
# -------------------------------------------------------------------------------
# ... archive
cd $HOME/weblibs/$1/esdoc-archive
git pull
source ./sh/activate
esdoc-archive-uncompress

# ... pyesdoc
cd $HOME/weblibs/$1/esdoc-py-client
git pull
source ./sh/activate

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
	cd $HOME/webapps/$1_fe_$_ESDOC_FRONT_END
	git pull
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
for _ESDOC_FRONT_END in "${_ESDOC_FRONT_ENDS[@]}"
do
	cd $HOME/webapps/$1_fe_$_ESDOC_FRONT_END
	git pull
done

# Reload daemons.
# ... cdf2cim
source $HOME/webapps/$1_ws_cdf2cim/sh/activate
cdf2cim-ws-daemon-reload

# ... documentation
source $HOME/webapps/$1_ws_documentation/sh/activate
esdoc-ws-daemon-reload

# ... errata
source $HOME/webapps/$1_ws_errata/sh/activate
errata-ws-daemon-reload

# ... url rewriter (doc)
source $HOME/webapps/$1_ws_url_rewriter_doc/sh/activate
rewriter-ws-daemon-reload

# ... url rewriter (further info)
source $HOME/webapps/$1_ws_url_rewriter_fi/sh/activate
rewriter-ws-daemon-reload

# -------------------------------------------------------------------------------
# Finalization
# -------------------------------------------------------------------------------
cd $HOME
