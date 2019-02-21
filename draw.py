import networkx as nx

class Graph():

    def __init__(self):
        self.graph = nx.DiGraph()

    def addMoneroAddress(self, address, balance, unlocked_balance, height, height_timestamp, label, used):
        self.graph.add_node(address, balance=balance, height=height, height_timestamp=height_timestamp, label=label, used=used)

    def write_result(self, file):
        nx.write_graphml(self.graph, file)

def generate_draw(w):

    g = Graph()

    adresses = w.addresses
    balances = w.balances

    for a in adresses:
        if a.index == 0:
            height = w.height
            height_timestamp = w.creation
        else:
            height = 0
            height_timestamp = 0

        for b in balances:
            if a.address == b.address:
                balance = b.balance
                unlocked_balance = b.unlocked
            g.addMoneroAddress(a.address, balance, unlocked_balance, height, height_timestamp, a.label, a.used)

    g.write_result("monero.graphml")
