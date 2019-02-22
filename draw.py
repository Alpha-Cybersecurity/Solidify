import networkx as nx
import random

class Graph():

    def __init__(self):
        self.graph = nx.DiGraph()

    def addWallet(self, w):
        wallet_name = "wallet:%s" % w.main_address.address
        self.graph.add_node(wallet_name, height=w.height, height_timestamp=w.creation, color='green')

        for a in w.addresses:
            self.addMoneroAddress(a)
            self.graph.add_path([wallet_name, a.address], color='green')

        for b in w.balances:
            self.addBalance(b)

        for o_tx in w.out_transfers:
            self.addMoneroTransaction(o_tx)

        for i_tx in w.in_transfers:
            self.addMoneroTransaction(i_tx)

    def addMoneroAddress(self, address):
        self.graph.add_node(address.address, description=address.label, used=address.used)

    def addBalance(self, balance):
        self.graph.node[balance.address]['balance'] = balance.balance
        self.graph.node[balance.address]['unlocked'] = balance.unlocked

    def addMoneroTransaction(self, tx):

        if tx.type == 'out':
            for destination in tx.destinations:
                self.graph.add_edge(tx.address, destination.address, txid=tx.txid, height=tx.height, timestamp=tx.timestamp, label=tx.note, amount=destination.amount, fee=tx.fee, weight=destination.amount, color='red')
        else:
            self.graph.add_edge("%010d" % random.randint(0, 1e10), tx.address, txid=tx.txid, height=tx.height, timestamp=tx.timestamp, label=tx.note, amount=tx.amount, fee=tx.fee, weight=tx.amount, color='blue')



    def write_result(self, file):
        nx.write_graphml(self.graph, file)

def generate_draw(w):

    g = Graph()
    g.addWallet(w)

    # balances = w.balances
    # out_transfers = w.out_transfers
    #
    # adresses = w.addresses
    # for a in adresses:
    #     g.addMoneroAddress(a)
    #
    #
    #     for b in balances:
    #         if a.address == b.address:
    #             balance = b.balance
    #             unlocked_balance = b.unlocked
    #             g.addMoneroAddress(a.address, balance, unlocked_balance, height, height_timestamp, a.label, a.used)
    #
    # for o_transfer in out_transfers:
    #     for destination in o_transfer.destinations:
    #         g.addMoneroTransaction(o_transfer.address, destination.address, destination.amount)

    g.write_result("monero.graphml")
