from flask import Flask
from flask.ext.restful import Api

from .resources.information import InformationResource
from .resources.mailbox import MailboxManagerResource
from .resources.mailbox import MailboxResource

app = Flask( __name__ )
api = Api( app )

api.add_resource( InformationResource, "/" )
api.add_resource( MailboxManagerResource, "/mailbox" )
api.add_resource( MailboxResource, "/mailbox/<string:name>" )
