
class Graph():

    def __init__(self):
        self.graph = nx.DiGraph()

    def addMoneroAddress(self, address, balance, unlocked_balance, height, height_timestamp, label, used):
        self.graph.add_node(address, balance=balance, height=height, height_timestamp=height_timestamp, label=label, used=used)

    def write_result(self, file):
        nx.write_graphml(self.graph, file)

def generate(mrpc):

    g = Graph()

    adresses = mrpc.getAddress().get('addresses')
    balances = mrpc.getBalance().get('per_subaddress')

    for a in adresses:
        if a.get('address_index') == 0:
            height = mrpc.getHeight()
            height_timestamp = mrpc.heightToDate(height)
        else:
            height = 0
            height_timestamp = 0
        for b in balances:
            if a.get('address') == b.get('address'):
                balance = b.get('balance')
                unlocked_balance = b.get('unlocked_balance')
            g.addMoneroAddress(a.get('address'), balance, unlocked_balance, height, height_timestamp, a.get('label'), a.get('used'))

    g.write_result("monero.graphml")
