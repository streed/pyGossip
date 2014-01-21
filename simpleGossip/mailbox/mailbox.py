import redis

class Mailbox( object ):
	
	def __init__( self, mailbox_name, **redis_settings ):
		self.mailbox = redis.Redis( **redis_settings )
		
		self.key = "simpleGossip:mailbox:%s" % mailbox_name
		
	def __len__( self ):
		return self.mailbox.llen( self.key )
		
	def empty( self ):
		return len( self ) == 0
		
	def put( self, letter ):
		self.mailbox.rpush( self.key, letter )
		
	def get( self, block=True, timeout=None ):
		if block:
			letter = self.mailbox.blpop( self.key, timeout=timeout )
		else:
			letter = self.mailbox.blpop( self.key )
			
		if letter:
			return letter[1]
		return letter
		
	def get_all( self, block=True, timeout=None ):
		letters = self.mailbox.lrange( self.key, 0, -1 )
		
		if letters:
			self.mailbox.delete( self.key )
			
		return letters