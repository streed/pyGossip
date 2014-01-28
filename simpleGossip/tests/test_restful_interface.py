import unittest

from ..app import app

from flask import json

class TestGossipingRestful( unittest.TestCase ):

  def setUp( self ):
    self.app = app.test_client()
    
  def test_get_gossiping_information( self ):
    info = self.app.get( "/" )

    info = json.loads( info.data )
    
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
                            'view': [],
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
                        
            
    def test_get_mailboxes_when_empty( self ):
        mailboxes = self.app.get( "/mailboxes" )

        self.assertEquals( { 
                            'status': 200,
                            'body':
                            {
                                'mailboxes': [] 
                            }
                        }, mailboxes )
