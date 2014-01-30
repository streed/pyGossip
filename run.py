from simpleGossip.gossiping.gossip import RemoteGossipService

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer( RemoteGossipService, port=18861 )
    t.start()
