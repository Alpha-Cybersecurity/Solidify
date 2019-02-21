class Wallet():

    def __init__(self, height):
        self.height = height

class Address():

    def __init__(self, address, label, used):
        self.address = address
        self.label = label
        self.used = used

    def __str__(self):
        return "Address %s (%s)" % (self.address, self.label)

class Balance():

    def __init__(self, address, balance, unlocked, num_unspent_outputs):
        self.address = address
        self.balance = balance
        self.unlocked = unlocked
        self.num_unspent_outputs = num_unspent_outputs

    def __str__(self):
        return "Balance (%s): %d" % (self.address, self.balance)

class Transfer():
    def __init__(self, address, amount, confirmations, double_spend_seen, fee, height, note, payment_id, timestamp, txid, type, destinations=[]):
        self.address = address
        self.amount = amount
        self.confirmations =  confirmations
        self.double_spend_seen = double_spend_seen
        self.fee =  fee
        self.height = height
        self.note =  note
        self.payment_id = payment_id
        self. timestamp =  timestamp
        self.txid = txid
        self.type = type

        if type=='out':
            self.destinations = destinations

    def add_destination(self, destination):
        if self.type != 'out':
            raise Exception("Destinations only for out transactions")

        self.destinations.append(destination)

    def __str__(self):
        if self.type == 'out':
            res = "%s =[%d]=>" % (self.address[:10], self.amount)
            for destination in self.destinations:
                res += "\n" + (" " * len(self.address[:10])) + " -(%d)-> %s\n" % (destination.amount, destination.address)
        else:
            res = "-(%d)-> %s" % (self.amount, self.address)

        return res

class Destination():
    def __init__(self, address, amount):
        self.address = address
        self.amount = amount
