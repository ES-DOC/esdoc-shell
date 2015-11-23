============================
ES-DOC shell - deployment commands
============================

esdoc-deploy-archive-compress
----------------------------

Compresses set of documents within local archive prior to deployment.

esdoc-deploy-archive-uncompress
----------------------------

Decompresses set of documents within local archive.

esdoc-deploy-compile-js-plugin
----------------------------

Compiles the ES-DOC javascript plugin.

**VERSION**

	Version of plugin to be compiled.

esdoc-deploy-display-active-shells
----------------------------

Displays the set of currently active shells upon the WebFacetion server.

esdoc-deploy-rollback
----------------------------

Rollbacks a previous deployment.

**ENVIRONMENT**

	test | prod

**VERSION**

	e.g. 0_9_0_1_1

	0 = Major identifier

	9 = Minor identifier

	0 = Revision identifier

	1 = Patch identifier

	1 = Deployment identifier


	**WEB-FACTION-MACHINE-NAME**

	Name of web faction server to which stack will be deployed.


	**WEB-FACTION-MACHINE-PASSWORD**

	Password of web faction server to which stack will be deployed.

	**API_DB_PWD**

	Password to be used to connect to API database upon WebFaction database server.

esdoc-deploy-rollout
----------------------------

Rollout a new deployment.

**ENVIRONMENT**

test | prod

**VERSION**

e.g. 0_9_0_1_1

0 = Major identifier
9 = Minor identifier
0 = Revision identifier
1 = Patch identifier
1 = Deployment identifier

**WEB-FACTION-MACHINE-NAME**

Name of web faction server to which stack will be deployed.

**WEB-FACTION-MACHINE-PASSWORD**

Password of web faction server to which stack will be deployed.

**API_DB_PWD**

Password to be used to connect to API database upon WebFaction database server.

esdoc-deploy-setup
----------------------------

Command to setup a shell for deployments.
