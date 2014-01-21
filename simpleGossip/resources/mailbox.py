import redis

from flask import jsonify
from flask.ext.restful import Resource

from ..mailbox.mailbox import Mailbox

class MailboxManagerResource( Resource ):

	def get( self ):
		r = redis.Redis()
		
		keys = r.keys( "simpleGossip:mailbox:*" )
		
		return keys
		
	def post( self ):
		return {}
		
class MailboxResource( Resource ):

	def get( self, name ):
		mailbox = Mailbox( name )
		
		letters = mailbox.get_all()
		
		return jsonify( status=200, body=letters )
		
	def post( self ):
		return {}