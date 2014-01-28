
class Router( object ):
    def __init__( self ):
        self.routes = {}

    def add_route( self, name, method ):
        """ This will add a new route or overwrite a current route in this Router.

            name - the name of this route.
            method - what function to call with the letter passed to it.
        """
        self.routes[name] = method

    def open( self, letter ):
        """ This method 'opens' a letter and acts on the contents.
            
            letter - the letter portion of a received letter.
        """
        return seflf.routes[letter["action"]]( letter["body"] )


