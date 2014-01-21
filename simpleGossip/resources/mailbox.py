import redis

from flask import jsonify, request
from flask.ext.restful import Resource

from ..mailbox.mailbox import Mailbox

class MailboxManagerResource( Resource ):

	def get( self ):
		r = redis.Redis()
		
		keys = r.keys( "simpleGossip:mailbox:*" )
		
		ret = []
		
		for k in keys:
			_, _, name = k.split( ":" )
			m = Mailbox( name )
			ret.append( dict( name=name, uri="http://127.0.0.1:5000/mailbox/%s" % name, total_messages=len( m ) ) )
		
		return jsonify( status=200, body=dict( mailboxes=ret ) )
		
	def post( self ):
		return {}
		
class MailboxResource( Resource ):

	def get( self, name ):
		mailbox = Mailbox( name )
		
		letters = mailbox.get_all()
		
		return jsonify( status=200, body=dict( letters=letters ) )
		
	def post( self, name ):
		letter = request.stream.read()
		
		mailbox = Mailbox( name )
		
		mailbox.put( letter )
		
		return {}