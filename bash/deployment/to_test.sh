# Update libs:

cd $HOME/weblibs/test

# ... archive
cd ./esdoc-archive
git pull
source ./sh/activate
esdoc-archive-uncompress

# ... pyesdoc
cd ../esdoc-py-client
git pull
source ./sh/activate

# Update web-service:
cd $HOME/webapps/test_ws_documentation
git pull
source ./sh/activate
esdoc-ws-daemon-reload
