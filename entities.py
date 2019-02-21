class Wallet():

    def __init__(self, mrpc):

        self.height = mrpc.getHeight()
        self.creation = mrpc.heightToDate(self.height)

        self.addresses = mrpc.getAddresses()
        self.balances = mrpc.getBalances()
        self.out_transfers = mrpc.getOutTransfers()
        self.in_transfers = mrpc.getInTransfers()

        # print(mrpc.getAccountsTags())
        # print(mrpc.getAddressBook())

class Address():

    def __init__(self, address, index, label, used):
        self.address = address
        self.index = index
        self.label = label
        self.used = used

class Balance():

    def __init__(self, address, balance, unlocked, num_unspent_outputs):
        self.address = address
        self.balance = balance
        self.unlocked = unlocked
        self.num_unspent_outputs = num_unspent_outputs


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


class Destination():
    def __init__(self, address, amount):
        self.address = address
        self.amount = amount
