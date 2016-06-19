#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import pika

class rabbit:
	def __init__(self,config):
		self.user = config['user']
		self.password = config['password']
		self.host = config['host']
		self.port = config['port']
		self.vhost = config['vhost']
		self.exchange = config['exchange']
		self.queue = config['queue']

		self.connection_init()

	def connection_init(self):
		credentials = pika.PlainCredentials(self.user, self.password)
		parameters = pika.ConnectionParameters(self.host, self.port, self.vhost, credentials)
		self.connection = pika.BlockingConnection(parameters)

	def consumer(self, callback):
		channel = self.connection.channel()
		channel.queue_declare(queue=self.queue, durable=True)

		# channel.basic_qos(prefetch_count=1) 因为可能会出错，当前不打开公平分发
		channel.basic_consume(callback, queue=self.queue)
		channel.start_consuming()

	def producer(self, message):
		channel = self.connection.channel()
		channel.exchange_declare(exchange=self.exchange, type='fanout')
		channel.queue_declare(queue=self.queue, durable=True)
		channel.queue_bind(exchange=self.exchange, queue=self.queue)

		# 设置confirm mode
		channel.confirm_delivery()

		r = channel.basic_publish(exchange=self.exchange,
									routing_key='',
									body=message,
									mandatory=True,
									properties=pika.BasicProperties(  
										delivery_mode = 2,
									))

		return (r, message)
