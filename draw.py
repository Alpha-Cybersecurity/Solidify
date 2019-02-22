from neo4j import GraphDatabase
import networkx as nx
import random

class Graph():

    def __init__(self):
        self.graph = nx.DiGraph()

    def addWallet(self, w):
        wallet_name = "wallet:%s" % w.main_address.address
        self.graph.add_node(wallet_name, address=w.main_address.address, height=w.height, height_timestamp=w.creation, color='#00eb3b')

        for a in w.addresses:
            self.addMoneroAddress(a)
            self.graph.add_path([wallet_name, a.address], color='black')

        for b in w.balances:
            self.addBalance(b)

        for o_tx in w.out_transfers:
            self.addMoneroTransaction(o_tx)

        for i_tx in w.in_transfers:
            self.addMoneroTransaction(i_tx)

    def addMoneroAddress(self, address):
        self.graph.add_node(address.address, address=address.address, description=address.label, used=address.used, color='#d1ffed')

    def addBalance(self, balance):
        self.graph.node[balance.address]['balance'] = balance.balance
        self.graph.node[balance.address]['unlocked'] = balance.unlocked

    def addMoneroTransaction(self, tx):

        if tx.type == 'out':
            for destination in tx.destinations:
                self.graph.add_edge(tx.address, destination.address, txid=tx.txid, label='transaction', height=tx.height, timestamp=tx.timestamp, note=tx.note, amount=destination.amount, fee=tx.fee, weight=destination.amount, color='#218DB1')
        else:
            self.unknownAddress = "%010d" % random.randint(0, 1e10)
            self.node = self.graph.add_node(self.unknownAddress , address=self.unknownAddress, color='#d3d3d3')
            self.graph.add_edge(self.unknownAddress, tx.address, txid=tx.txid, label='transaction', height=tx.height, timestamp=tx.timestamp, note=tx.note, amount=tx.amount, fee=tx.fee, weight=tx.amount, color='#ff2400')

    def write_result(self, file):
        nx.write_graphml(self.graph, file)

class Neo4j():

    def __init__(self, driver):
        self.session = driver.session()
    
    def addWallet(self, w):
        wallet_name = "wallet:%s" % w.main_address.address
        self.session.run("CREATE (a:Wallet {name: $wallet_name, address: $address, height: $height, height_timestamp: $height_timestamp }) ",
        wallet_name=wallet_name, address=w.main_address.address, height=w.height,height_timestamp=w.creation)

        for a in w.addresses:
            self.addMoneroAddress(a, wallet_name)

    def addMoneroAddress(self, address, wallet_name):
        self.session.run("MERGE (a:Address {address: $address}) "
           "MERGE (a)-[:BELONG]->(wallet:Wallet {name: $wallet_name})",
           address=address.address, wallet_name=wallet_name)


def generate_draw(w, output):

    g = Graph()
    g.addWallet(w)

    g.write_result(output)

def insert_neo4j(w, neoHost, neoPort, neoUser ,neoPassword):
    driver = GraphDatabase.driver("bolt://" +  neoHost + ":" + neoPort, auth=(neoUser, neoPassword))
    
    n = Neo4j(driver)
    n.addWallet(w)
