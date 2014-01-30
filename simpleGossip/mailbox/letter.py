
class Letter( object ):

    def __init__( self ):
        pass

class NewNodeLetter( Letter ):
    def __init__( self, node):
        super( NewNodeLetter, self ).__init__()

        self.node = node

class DeadNodeLetter( NewNodeLetter ):
    def __init__( self,  node ):
        super( DeadNewNodeLetter, self ).__init__( node )

class ViewLetter( Letter ):
    def __init__( self, view ):
        super( ViewLetter, self ).__init__()

        self.view = view

class SuccessLetter( Letter ):
    pass

class ErrorLetter( Letter ):
    def __init__( self, message ):
        super( ErrorLetter, self ).__init__()
        self.message = message
