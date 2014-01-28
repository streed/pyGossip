import unittest

from ..app import app

from flask import json

class TestGossipingRestfulEmpty( unittest.TestCase ):

    def setUp( self ):
        self.maxDiff = None
        self.app = app.test_client()

    def test_get_gossiping_information( self ):
        info = self.app.get( "/" )

        info = json.loads( info.data )

        self.assertEquals( { 
            u'status': 200, 
            u'body': 
            { 
                u'fanout': 10, 
                u'total_nodes': 0, 
                u'total_letters_sent': 0, 
                u'total_letters_received': 0, 
                u'total_healthy_nodes': 0, 
                u'total_unhealthy_nodes': 0, 
                u'neighborhood': [],
                u'mailboxes': [] 
                } 
            }, info )

    def test_get_mailboxes_when_empty( self ):
        mailboxes = self.app.get( "/mailbox" )
        mailboxes = json.loads( mailboxes.data )
        self.assertEquals( { 
            u'status': 200,
            u'body':
            {
                u'mailboxes': [] 
            }
          }, mailboxes )


class TestGossipingRestfulMailbox( unittest.TestCase ):

    def setUp( self ):
        self.maxDiff= None
        self.app = app.test_client()

    def test_create_mailbox( self ):
        mailbox = self.app.post( "/mailbox", data=dict(
                                                        sender="127.0.0.1",
                                                        ttl=-1,
                                                        letter=dict(
                                                                    action="new_mailbox",
                                                                    body=dict(
                                                                                name="ants",
                                                                                size=100,
                                                                                methods=[
                                                                                            "election",
                                                                                            "append_entries",
                                                                                            "new_term" ]))))

