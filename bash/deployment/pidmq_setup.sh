# http://aameer.github.io/installing-rabbitmq-on-webfaction/
# http://www.markliu.me/2011/sep/29/django-celery-on-webfaction-using-rabbitmq/
# https://community.webfaction.com/questions/17426/tutorial-django-celery-rabbitmq-virtualenv
# https://www.rabbitmq.com/management.html
# https://raw.githubusercontent.com/rabbitmq/rabbitmq-server/master/docs/rabbitmq.config.example

setup_erlang()
{
	# $1 = test|prod
	# #2 = erlang port number

	# Download & unzip.
	cd webapps/$1_mq_erlang
	wget http://erlang.org/download/otp_src_19.2.tar.gz
	gunzip -c otp_src_19.2.tar.gz | tar xf -

	# Build & install.
	cd ./otp_src_19.2
	./configure --prefix=/home/esdoc/
	make
	make install

	# Run daemon process
	epmd -port $2 -daemon
}

setup_rabbitmq()
{
	# $1 = test|prod
	# #2 = RabbitMQ version
	cd webapps/$1_mq_rabbit
	wget http://www.rabbitmq.com/releases/rabbitmq-server/v3.6.9/rabbitmq-server-generic-unix-3.6.9.tar.xz
	tar xf ./rabbitmq-server-generic-unix-3.6.9.tar.xz
	pwd /home/esdoc/webapps/test_mq_rabbit
	ln -s /home/esdoc/webapps/test_mq_rabbit/rabbitmq_server-3.6.9 ~/lib/erlang/lib/

	setup_rabbitmq_defaults
	setup_rabbitmq_env
	setup_erlang_hosts
	setup_erlang_inetrc

	cd ./rabbitmq_server-3.6.9/sbin
	./rabbitmq-server -detached
	./rabbitmqctl status

	./rabbitmqctl add_user node-admin kVweE6u2PC6W9JjpCuEKJCnDYS8BCsX8
	./rabbitmqctl add_user esgf-publisher LDfj5784T4VeKTxwhpqk8UmSqbC9DkTW
	./rabbitmqctl add_user esgf-downstream qfwSeEjrPTZdfqbFLv7VqgSXzbnXD6Qr

	./rabbitmqctl set_user_tags node-admin adminstrator

	./rabbitmqctl add_vhost esgf-pid

	./rabbitmqctl set_permissions node-admin ".*" ".*" ".*"
	./rabbitmqctl set_permissions -p esgf-pid node-admin ".*" ".*" ".*"
	./rabbitmqctl set_permissions -p esgf-pid esgf-publisher "" ".*" ""
	./rabbitmqctl set_permissions -p esgf-pid esgf-downstream ".*" ".*" ".*"
}

setup_rabbitmq_defaults()
{
	vi ./rabbitmq_server-3.6.9/sbin/rabbitmq-defaults
	vi rabbitmq-defaults
	# CONFIG_FILE=/home/esdoc/webapps/test_mq_rabbit/rabbitmq_server-3.6.9/sbin
	# LOG_BASE=/home/esdoc/logs/user/test_mq_rabbit
	# MNESIA_BASE=/home/esdoc/webapps/test_mq_rabbit/rabbitmq_server-3.6.9/sbin
}

setup_rabbitmq_env()
{
	vi ./rabbitmq_server-3.6.9/sbin/rabbitmq-env
	# export ERL_EPMD_PORT=15360
	
	# export ERL_INETRC=$HOME/.erl_inetrc
}

setup_erlang_hosts()
{
	# NOTE - immutable across envs.
	vi $HOME/hosts
	# 127.0.0.1 localhost.localdomain localhost
	# ::1 localhost6.localdomain6 localhost6
	# 127.0.0.1 75.126.149.11 75.126.149.11.webfaction.com
}

setup_erlang_inetrc()
{
	# NOTE - immutable across envs.
	vi $HOME/.erl_inetrc
	# {hosts_file, "/home/esdoc/hosts"}.
	# {lookup, [file,native]}.
}
