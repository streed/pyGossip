import redis

class Mailbox( object ):
    def __init__( self, mailbox_name ):
        self.name = mailbox_name

    def empty( self ):
        pass

    def put( self, letter ):
        pass

    def get( self ):
        pass

    def get_all( self ):
        pass

    def __len__( self ):
        return 0

class MemoryMailbox( Mailbox ):
    def __init__( self, mailbox_name ):
        super( Mailbox, self ).__init__( mailbox_name )

        self.mailbox = []

    def __len__( self ):
        return len( self.mailbox )

    def empty( self ):
        return len( self ) == 0

    def put( self, letter ):
        self.mailbox.append( letter )

        return True

    def get( self ):
        return self.mailbox.pop( 0 )

    def get_all( self ):
        ret = self.mailbox[:]
        self.mailbox = []

        return ret

class RedisMailbox( Mailbox ):
	
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
		return self.mailbox.rpush( self.key, letter )
		
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
				
		return ret

