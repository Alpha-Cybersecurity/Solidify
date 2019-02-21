from entities import Wallet, Address, Balance, Transfer, Destination

def parse(mrpc):

    height = mrpc.getHeight()
    w = Wallet(height)

    # print(mrpc.getAccountsTags())
    print(mrpc.getAddressBook())
