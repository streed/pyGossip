from ..mailbox.mailbox import Mailbox
from ..mailbox.router import Router

class Gossip( object ):

    def __init__( self, seed=[], fanout=10 )
        self.router = Router()
        self.total_nodes = 0
        self.total_letters_sent = 0
        self.total_letters_received = 0
        self.total_healthy_nodes = 0
        self.total_unhealthy_nodes = 0

        self.system = Mailbox( "system" )
