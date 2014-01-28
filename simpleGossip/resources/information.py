import redis

from flask import jsonify
from flask.ext.restful import Resource

from ..gossiping.gossip import Gossip

class InformationResource( Resource ):

	def get( self ):
		gossip = Gossip()

                gossip_dict = gossip.to_dict()

                temp = []

		r = redis.Redis()
		
		keys = r.keys( "simpleGossip:mailbox:*" )

		for k in keys:
			_, _, name = k.split( ":" )
			m = Mailbox( name )
			temp.append( dict( name=name, uri="http://127.0.0.1:5000/mailbox/%s" % name, total_messages=len( m ) ) )

                gossip_dict["mailboxes"] = temp

                return jsonify( status= 200, body=gossip_dict )	
