import rpyc
from ..mailbox.mailbox import RedisMailbox
from ..mailbox.letter import SuccessLetter, ErrorLetter, ViewLetter

class GossipService( object ):
    def __init__( self, seed=[], fanout=10 ):
        pass
    
class RemoteGossipService( GossipService, rpyc.Service ):

    def __init__( self, seed=[], fanout=10 ):
        super( RemoteGossipService, self ).__init__( seed=seed, fanout=fanout )

    def on_connect( self ):
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

    def exposed_new_node( self, letter ):
        if self.mailboxes["system"].put( letter ):
            return SuccessLetter()
        else:
            return ErrorLetter( "Could not save letter" )

    def exposed_dead_node( self, letter ):
        return letter

    def exposed_view( self, letter ):
        print dir( letter.view )

        return ViewLetter( self.neighborhood )

    def exposed_info( self ):
        return dict(
                    fanout=self.fanout,
                    neighborhood=self.neighborhood,
                    total_nodes=self.total_nodes,
                    total_letters_sent=self.total_letters_sent,
                    total_letters_received=self.total_letters_received,
                    total_healthy_nodes=self.total_healthy_nodes,
                    total_unhealthy_nodes=self.total_unhealthy_nodes )

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

    def __init__( self, name ):
        super( RemoteGossipServiceClient, self ).__init__( name )

        self.conn = rpyc.connect( self.name, 18861 )

    def new_node( self, letter ):
        return self.conn.root.new_node( letter )

    def dead_node( self, letter ):
        return self.conn.root.dead_node( letter )

    def view( self, letter ):
        return self.conn.root.view( letter )

    def info( self ):
        return self.conn.root.info()

