import requests
import random
import subprocess
import time
import signal
from entities import Wallet, Address, Balance, Transfer, Destination

class MoneroRPC:

    #monero-wallet-rpc.exe --stagenet --password "" --rpc-bind-port 28088 --disable-rpc-login  --daemon-host monero-stagenet.exan.tech:38081  --wallet-file C:\Users\carlos\Documents\Monero\wallets\carlos-stagenet\carlos-stagenet#init method and start monero-wallet-rpc

    def __init__(self, host, port, wallet_file=None, exe=None):

        self._proxy_host = host
        self._proxy_port = port # Puerto aleatorio para poder lanzar varios

        if exe:
            if not wallet_file:
                raise Exception("No wallet file specified")

            command = [exe]
            options = dict(
                disable_login = '--disable-rpc-login',
                net = '--stagenet',
                password = '--password ""',
                rpc_port = '--rpc-bind-port %d' % (self._proxy_port),
                daemon_host = '--daemon-host monero-stagenet.exan.tech:38081',
                wallet_dit = '--wallet-file "%s"' % wallet_file # C:\Users\carlos\Documents\Monero\wallets\carlos-stagenet
            )
            print(options)
            command += ["%s" % v for v in options.values()]

            # TODO Ver output
            print(" ".join(command))
            self._p = subprocess.Popen(" ".join(command))
            self.start_close_handler()

            time.sleep(5)


    def start_close_handler(self):
        signal.signal(signal.SIGINT, self.end)
        signal.signal(signal.SIGSEGV, self.end)
        signal.signal(signal.SIGFPE, self.end)
        signal.signal(signal.SIGABRT, self.end)
        signal.signal(signal.SIGILL, self.end)

    def end(self, signum, *args):
        print('Signal handler called with signal %s' % signum)
        self._p.terminate()

    @property
    def proxy_address(self):
        addr = "http://%s:%d" % (self._proxy_host, self._proxy_port)
        return addr

    @property
    def json_rpc_address(self):
        return "%s/json_rpc" % self.proxy_address

    def getAddress(self):

        headers = {
            'Content-Type': 'application/json',
        }

        data = '{"jsonrpc":"2.0","id":"0","method":"get_address","params":{"account_index":0}}'

        response = requests.post(self.json_rpc_address, headers=headers, data=data)
        r_data = response.json().get('result')

        addresses = []
        for a in r_data['addresses']:
            address = Address(a.get('address'), a.get('label'), a.get('used'))
            addresses.append(address)

        return addresses

    def getBalances(self):

        headers = {
            'Content-Type': 'application/json',
        }

        data = '{"jsonrpc":"2.0","id":"0","method":"get_balance","params":{"account_index":0,"address_indices":[0,1]}}'

        response = requests.post(self.json_rpc_address, headers=headers, data=data)
        r_data = response.json().get('result')

        balances = []
        for b in r_data['per_subaddress']:
            balance = Balance(b.get('address'), b.get('balance'), b.get('unlocked_balance'), b.get('num_unspent_outputs'))
            print(balance)
            balances.append(balance)

        return balances

    def getAccountsTags(self):

        headers = {
            'Content-Type': 'application/json',
        }

        data = '{"jsonrpc":"2.0","id":"0","method":"get_accounts"}'

        response = requests.post(self.json_rpc_address, headers=headers, data=data)

        # TODO Parse result
        return response.json().get('result')

    def getHeight(self):

        headers = {
            'Content-Type': 'application/json',
        }

        data = '{"jsonrpc":"2.0","id":"0","method":"get_height"}'

        response = requests.post(self.json_rpc_address, headers=headers, data=data)
        r_data = response.json().get('result')

        return r_data.get('height')

    def heightToDate(self, height):

        r = requests.get('https://moneroblocks.info/api/get_block_header/' + str(height))
        r_data = r.json().get('block_header')

        return r_data.get('timestamp')

    def getAddressBook(self):

        headers = {
            'Content-Type': 'application/json',
        }

        data = '{"jsonrpc":"2.0","id":"0","method":"get_address_book","params":{}}'

        response = requests.post(self.json_rpc_address, headers=headers, data=data)

        # TODO Parse result
        return response.json().get('result').get('entries')

    def getOutTransfers(self):

        headers = {
            'Content-Type': 'application/json',
        }

        data = '{"jsonrpc":"2.0","id":"0","method":"get_transfers","params":{"out":true}}'

        response = requests.post(self.json_rpc_address, headers=headers, data=data)
        r_data = response.json().get('result')

        out_transfers = []
        for t in r_data.get('out'):
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

            out_transfers.append(transfer)

        return out_transfers

    def getInTransfers(self):

        headers = {
            'Content-Type': 'application/json',
        }

        data = '{"jsonrpc":"2.0","id":"0","method":"get_transfers","params":{"in":true}}'

        response = requests.post(self.json_rpc_address, headers=headers, data=data)
        r_data = response.json().get('result')

        in_transfers = []
        for t in r_data.get('in'):
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

        return in_transfers
