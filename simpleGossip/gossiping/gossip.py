import rpyc
from ..mailbox.mailbox import RedisMailbox
from ..mailbox.letter import SuccessLetter, ErrorLetter, ViewLetter

class GossipService( object ):
    def __init__( self, seed=[], fanout=10 ):
        pass
    
class RemoteGossipService( GossipService, rpyc.Service ):

    initialized = False

    def __init__( self, seed=[], fanout=10 ):
        super( RemoteGossipService, self ).__init__( seed=seed, fanout=fanout )

    def on_connect( self ):
        if not self.initialized:
            self.total_nodes = 0
            self.total_letters_sent = 0
            self.total_letters_received = 0
            self.total_healthy_nodes = 0
            self.total_unhealthy_nodes = 0


            self.mailboxes = {}
            self.mailboxes["system"] = RedisMailbox( "system" )

            self.neighborhood = []
            self.fanout = 10

    def on_disconnect( self ):
        pass

    def exposed_new_node( self, node ):
        """
            This takes the passed in node and wraps it up and sends it to
            the mailbox.

            self - Is defined.
            node - is a string representing either a ip or a hostname.
        """
        return self.store_letter( "system", NewNodeLetter( node ) )

    def exposed_dead_node( self, node ):
        """
            This takes the passed in node and wraps it up and sends it to
            the mailbox.

            self - Is defined.
            node - is a string representing either a ip or a hostname.
        """
        return self.store_letter( "system", DeadNodeLetter( node ) ):

    def exposed_view( self, view ):
        """
            This takes the passed in node and wraps it up and sends it to
            the mailbox.

            self - Is defined.
            node - is a string representing either a ip or a hostname.
        """
        return self.store_letter( "system", ViewLetter( view ) ):

    def exposed_get_letters( self, mailbox ):
        """
            This will return the letters for a specific mailbox.

            self - Is defined.
            mailbox - a string representing a mailbox.
        """
        return self.get_letters( mailbox )

    def exposed_application_letter( self, mailbox, body ):
        """
            This is used to send an application specific, i.e a message
            destined for a mailbox other than system.

            self - Is defined.
            mailbox - is a string representing a mailbox 
            body - the data for this message.
        """
        if mailbox in self.mailboxes and mailbox != "system":
            self.mailboxes[mailbox].put( ApplicationLetter( body ) ) 

    def exposed_broadcast( self, letter ):
        """
            When called this will broadcast out a message to all nodes in
            this neighborhood.

            self - Is defined.
            letter - Is defined.
        """
        for n in self.neighborhood:
            self.total_letters_sent += 1
            n.application_letter( letter["mailbox"], letter["body"] )

    def exposed_info( self ):
        return dict(
                    fanout=self.fanout,
                    neighborhood=self.neighborhood,
                    total_nodes=self.total_nodes,
                    total_letters_sent=self.total_letters_sent,
                    total_letters_received=self.total_letters_received,
                    total_healthy_nodes=self.total_healthy_nodes,
                    total_unhealthy_nodes=self.total_unhealthy_nodes )

    def store_letter( self, letter ):
        self.total_letters_received += 1
        return self.mailboxes[mailbox].put( letter )

    def get_letters( self, mailbox ):
        return self.mailboxes[mailbox].get_all()

class GossipServiceClient( object ):

    def __init__( self, name ):
        self.name = name
    
    def new_node( self, letter ):
        pass

    def dead_node( self, letter ):
        pass

    def view( self, letter ):
        pass

    def info( self ):
        pass

class LocalTestGossipServiceClient( GossipServiceClient ):
    def __init__( self, name, service ):
        super( GossipServiceClient, self ).__init__( name )

        self.service = service

    def new_node( self, letter ):
        return self.service.new_node( letter )

    def dead_node( self, letter ):
        return self.service.dead_node( letter )

    def view( self, letter ):
        return self.service.view( letter )

    def info( self ):
        return self.service.info()

class RemoteGossipServiceClient( GossipServiceClient ):
    results = []

    def __init__( self, name ):
        super( RemoteGossipServiceClient, self ).__init__( name )

        self.conn = rpyc.connect( self.name, 18861 )

    def new_node( self, letter ):
        ret = self.conn.root.new_node( letter )

        if ret:
            pass
        else:
            pass
        
    def dead_node( self, letter ):
        ret = self.conn.root.dead_node( letter )

        if ret:
            pass
        else:
            pass

    def view( self, letter ):
        ret = self.conn.root.view( letter )

        if ret:
            pass
        else:
            pass

    def info( self ):
        return self.conn.root.info()

