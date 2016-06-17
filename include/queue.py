#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import pika

class rabbit:
	def __init__(self):
		self.user = 'user_nsis'
		self.password = 'npass234!'
		self.host = '192.168.2.118'
		self.port = 5672
		self.vhost = '/nsis'
		self.exchange = 'ex_nsis'
		self.queue = 'q_nsis_1'

		self.connection_init()

	def connection_init(self):
		credentials = pika.PlainCredentials(self.user, self.password)
		parameters = pika.ConnectionParameters(self.host, self.port, self.vhost, credentials)
		self.connection = pika.BlockingConnection(parameters)

	def consumer(self, callback):
		channel = self.connection.channel()
		channel.queue_declare(queue=self.queue)

		channel.basic_consume(callback, queue=self.queue)
		channel.start_consuming()

	def producer(self, message):
		channel = self.connection.channel()
		channel.exchange_declare(exchange=self.exchange, type='fanout')
		channel.queue_declare(queue=self.queue)
		channel.queue_bind(exchange=self.exchange, queue=self.queue)

		# 设置confirm mode
		channel.confirm_delivery()

		r = channel.basic_publish(exchange=self.exchange, routing_key='', body=message, mandatory=True)

		return (r, message)
