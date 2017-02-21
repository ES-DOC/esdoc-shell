# -------------------------------------------------------------------------------
# Update libs
# -------------------------------------------------------------------------------

echo $1

# ... archive
# cd $HOME/weblibs/test/esdoc-archive
# git pull
# source ./sh/activate
# esdoc-archive-uncompress

# # ... pyesdoc
# cd $HOME/weblibs/test/esdoc-py-client
# git pull
# source ./sh/activate

# # -------------------------------------------------------------------------------
# # Update front-ends
# # -------------------------------------------------------------------------------
# # ... compare
# cd $HOME/webapps/test_fe_compare
# git pull

# # ... demo
# cd $HOME/webapps/test_fe_demo
# git pull

# # ... errata
# cd $HOME/webapps/test_fe_errata
# cp $HOME/webapps/test_fe_errata/search.html $HOME/webapps/test_fe_errata/index.html
# git pull

# # ... search
# cd $HOME/webapps/test_fe_search
# git pull

# # ... splash
# cd $HOME/webapps/test_fe_splash
# git pull

# # ... static
# cd $HOME/webapps/test_fe_static
# git pull

# # ... view
# cd $HOME/webapps/test_fe_view
# git pull

# # -------------------------------------------------------------------------------
# # Update web-services
# # -------------------------------------------------------------------------------
# # ... cdf2cim
# cd $HOME/webapps/test_ws_cdf2cim
# git pull
# source ./sh/activate
# cdf2cim-ws-daemon-reload

# # ... documentation
# cd $HOME/webapps/test_ws_documentation
# git pull
# source ./sh/activate
# esdoc-ws-daemon-reload

# # ... errata
# cd $HOME/webapps/test_ws_errata
# git pull
# source ./sh/activate
# errata-ws-daemon-reload

# # ... url rewriter (doc)
# cd $HOME/webapps/test_ws_url_rewriter_doc
# git pull
# source ./sh/activate
# rewriter-ws-daemon-reload

# # ... url rewriter (further info)
# cd $HOME/webapps/test_ws_url_rewriter_fi
# git pull
# source ./sh/activate
# rewriter-ws-daemon-reload
