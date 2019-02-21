from entities import Wallet, Address, Balance, Transfer, Destination

def parse(mrpc):

    w = Wallet(mrpc)
    return w
    # print(mrpc.heightToDate(height))
    # print(mrpc.getAccountsTags())
    # print(mrpc.getAddressBook())
