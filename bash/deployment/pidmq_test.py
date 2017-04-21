# -*- coding: utf-8 -*-

"""
.. module:: pidmq_test.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Test publishing / consumption of message to IPSL RabbitMQ server for ESGF-PID.

.. moduleauthor:: Mark Greenslade <momipsl@ipsl.jussieu.fr>

"""
import argparse
import os
import pika



# Define command line options.
_ARGS = argparse.ArgumentParser("Interacts with IPSL ESGF-PID RabbitMQ server.")
_ARGS.add_argument(
    "--action",
    help="Action to test.",
    dest="action",
    type=str
    )

# RabbitMQ server connection parameters.
_RABBITMQ_SERVER = '207.38.94.86:32272'
_RABBITMQ_VHOST = 'esgf-pid'

# Note: passwords passed in via environment variables.
_PWD_PUBLISHER = os.getenv('ESGF_PID_PUBLISHER_PWD')
_PWD_DOWNSTREAM = os.getenv('ESGF_PID_DOWNSTREAM_PWD')


def _publish():
	"""Publish test message.

	"""
	addr = 'amqp://esgf-publisher:{}@{}/{}'.format(_PWD_PUBLISHER, _RABBITMQ_SERVER, _RABBITMQ_VHOST)
	parameters = pika.URLParameters(addr)
	connection = pika.BlockingConnection(parameters)
	channel = connection.channel()
	channel.queue_bind(
		queue="test-queue",
		exchange="test-exchange",
		routing_key="*"
		)
	channel.basic_publish(
		'test-exchange',
	    'test_routing_key',
	    'message body value',
	    pika.BasicProperties(content_type='text/plain', delivery_mode=1)
	    )
	connection.close()


def _on_message(channel, method_frame, header_frame, body):
    print method_frame.delivery_tag
    print body
    print
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


def _consume():
	"""Consume test message.

	"""
	addr = 'amqp://esgf-downstream:{}@{}/{}'.format(_PWD_DOWNSTREAM, _RABBITMQ_SERVER, _RABBITMQ_VHOST)
	parameters = pika.URLParameters(addr)
	connection = pika.BlockingConnection(parameters)
	channel = connection.channel()
	channel.basic_consume(_on_message, 'test-queue')
	try:
	    channel.start_consuming()
	except KeyboardInterrupt:
	    channel.stop_consuming()
	connection.close()


def _main(args):
    """Main entry point.

    """
    if args.action in {'p', 'publish'}:
    	_publish()
    elif args.action in {'c', 'consume'}:
    	_consume()
    else:
    	raise ValueError("Invalid action")


# Entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
