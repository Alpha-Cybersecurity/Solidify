from entities import Address, Balance, Transfer, Destination

def parse(mrpc):

    print("[*] Addresses")

    addresses = []
    for a in mrpc.getAddress()['addresses']:
        address = Address(a.get('address'), a.get('label'), a.get('used'))
        print(address)
        addresses.append(address)

    print("[*] Balances")

    balances = []
    for b in mrpc.getBalance()['per_subaddress']:
        balance = Balance(b.get('address'), b.get('balance'), b.get('unlocked_balance'), b.get('num_unspent_outputs'))
        print(balance)
        balances.append(balance)

    height = mrpc.getHeight().get('height')

    print("[*] Out Transfers")

    out_transfers = []
    for t in mrpc.getOutTransfers():
        transfer = Transfer(
            t.get('address'),
            t.get('amount'),
            t.get('confirmations'),
            t.get('double_spend_seen'),
            t.get('fee'),
            t.get('height'),
            t.get('note'),
            t.get('payment_id'),
            t.get('timestamp'),
            t.get('txid'),
            t.get('type')
        )
        for d in t.get('destinations'):
            destination = Destination(d.get('address'), d.get('amount'))
            transfer.add_destination(destination)
        print(transfer)

        out_transfers.append(transfer)

    print("[*] In Transfers")

    in_transfers = []
    for t in mrpc.getInTransfers():
        transfer = Transfer(
            t.get('address'),
            t.get('amount'),
            t.get('confirmations'),
            t.get('double_spend_seen'),
            t.get('fee'),
            t.get('height'),
            t.get('note'),
            t.get('payment_id'),
            t.get('timestamp'),
            t.get('txid'),
            t.get('type')
        )
        print(transfer)
        in_transfers.append(transfer)
