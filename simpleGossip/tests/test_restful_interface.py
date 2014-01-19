import unittest

from ..app import app

class TestGossipingRestful( unittest.TestCase ):

  def setUp( self ):
    self.app = app.test_client()
    
  def test_get_gossiping_information( self ):
    info = self.app.get( "/" )
    
    self.assertEquals( { 
                          'status': 200, 
                          'body': 
                          { 
                            'fanout': 10, 
                            'total_nodes': 0, 
                            'total_letters_sent': 0, 
                            'total_letters_received': 0, 
                            'total_healthy_nodes': 0, 
                            'total_unhealthy_nodes': 0, 
                            'view': []
                            'mailboxes': 
                            [ 
                              { 
                                'name': 'system', 
                                'mailbox_size': 100, 
                                'mailbox_queue': 0
                              } 
                            ] 
                          } 
                        }, info )
                        
            
