from ..mailbox.mailbox import Mailbox
from ..mailbox.router import Router

class Gossip( object ):

    def __init__( self, router=None seed=[], fanout=10 )
        self.router = router
        self.total_nodes = 0
        self.total_letters_sent = 0
        self.total_letters_received = 0
        self.total_healthy_nodes = 0
        self.total_unhealthy_nodes = 0

        self.system = Mailbox( "system" )

        self.neighborhood = seed
        self.fanout = fanout

        if( self.router ):
            self.router.add_route( "new_node", self.new_node )
            self.router.add_route( "dead_nodea", self.dead_node )
            self.router.add_route( "view", self.view )


    def new_node( self, letter ):
        return letter

    def dead_node( self, letter ):
        return letter

    def view( self, letter ):
        return letter

    def to_dict( self ):
        return dict(
                    fanout=self.fanout,
                    neighborhood=self.neighborhood,
                    total_nodes=self.total_nodes,
                    total_letters_sent=self.total_letters_sent,
                    total_letters_received=self.total_letters_received,
                    total_healthy_nodes=self.total_healthy_nodes,
                    total_unhealthy_nodes=self.total_unhealthy_nodes )
