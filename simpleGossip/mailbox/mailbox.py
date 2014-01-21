import redis

from flask import json

from schema import Schema, And, Use, Optional

Letter = Schema( And( Use( json.loads ),
					{ "sender": And( basestring, len ),
					"ttl": And( Use( int ), lambda n: n >= -1 ),
					"timestamp": Use( int ),
					"letter": object } ) )

class Mailbox( object ):
	
	def __init__( self, mailbox_name, **redis_settings ):
		self.mailbox = redis.Redis( **redis_settings )
		
		self.key = "simpleGossip:mailbox:%s" % mailbox_name
		
	def __len__( self ):
		"""Python magic method to allow the use of the len builtin."""
		return self.mailbox.llen( self.key )
		
	def empty( self ):
		"""Wrapper to test if the length of the queue is 0."""
		return len( self ) == 0
		
	def put( self, letter ):
		"""This takes a raw string version of the letter then validates it
		and finally dumps it into the proper json format and saves it to the
		queue."""
		out = Letter.validate( letter )
		self.mailbox.rpush( self.key, json.dumps( out ) )
		
	def get( self, block=True, timeout=None ):
		""" This will return the top most letter from the queue."""
		if block:
			letter = self.mailbox.blpop( self.key, timeout=timeout )
		else:
			letter = self.mailbox.blpop( self.key )
			
		if letter:
			return letter[1]
		return letter
		
	def get_all( self, block=True, timeout=None ):
		"""This will return the entire queue for the current mailbox."""
		letters = self.mailbox.lrange( self.key, 0, -1 )
		
		if letters:
			self.mailbox.delete( self.key )
			
		ret = []
		
		for l in letters:
			out = Letter.validate( l )
			ret.append( out )
			
		return ret