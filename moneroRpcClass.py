import requests
import subprocess
import time
import signal
from entities import Address, Balance, Transfer, Destination


class Requester():

    def __init__(self, proxy_host, proxy_port):
        self.json_rpc_address = "http://%s:%d/json_rpc" % (proxy_host, proxy_port)

    def gen_request_data(self, method, params=None):

        res = dict(
            jsonrpc="2.0",
            id=0,
            method=method
        )

        if params:
            res['params'] = params

        return res

    def gen_request(self, method, params=None):

        data = self.gen_request_data(method, params)

        response = requests.post(self.json_rpc_address, json=data)

        if response.status_code != 200:
            raise Exception("[%d] Error sending %s (%s)" % (response.status_code, method, params))

        # TODO Evaluate response status_code
        r_data = response.json().get('result', None)

        if not r_data:
            raise Exception("None response in %s (%s)" % (method, params))

        return r_data

    def get_addresses(self):
        method = "get_address"

        params = dict(
            account_index=0
        )

        response = self.gen_request(method, params=params)

        return response

    def get_balances(self):
        method = "get_balance"

        params = dict(
            account_index=0,
            address_indices=[0, 1] # TODO Add other indices
        )

        response = self.gen_request(method, params=params)

        return response

    def get_accounts_tags(self):
        method = "get_accounts"

        response = self.gen_request(method)

        return response

    def get_height(self):
        method = "get_height"

        response = self.gen_request(method)

        return response

    def get_address_book(self):
        method = "get_address_book"

        params = dict()

        response = self.gen_request(method, params=params)

        return response

    def get_in_transfers(self):
        method = "get_transfers"

        # Es necesario hacerlo así porque 'in' es palabra reservada en python
        params = dict()
        params['in'] = True

        response = self.gen_request(method, params=params)

        return response

    def get_out_transfers(self):
        method = "get_transfers"

        params = dict(
            out=True
        )

        response = self.gen_request(method, params=params)

        return response


class MoneroRPC:
    def __init__(self, host, port, wallet_file=None, exe=None):

        self._proxy_host = host
        self._proxy_port = port  # Puerto aleatorio para poder lanzar varios?

        self._requester = Requester(host, port)

        if exe:
            '''
            monero-wallet-rpc.exe
                --stagenet --password ""
                --rpc-bind-port 28088
                --disable-rpc-login
                --daemon-host monero-stagenet.exan.tech:38081
                --wallet-file C:\\Users\\carlos\\Documents\\Monero\\wallets\\carlos-stagenet\\carlos-stagenet#init method and start monero-wallet-rpc
            '''
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

            command += ["%s" % v for v in options.values()]

            # TODO Ver output
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

    def getAddresses(self):

        r_data = self._requester.get_addresses()

        addresses = []
        for a in r_data['addresses']:
            address = Address(a.get('address'), a.get('address_index'), a.get('label'), a.get('used'))
            addresses.append(address)

        return addresses

    def getBalances(self):

        r_data = self._requester.get_balances()

        balances = []
        for b in r_data['per_subaddress']:
            balance = Balance(b.get('address'), b.get('balance'), b.get('unlocked_balance'), b.get('num_unspent_outputs'))
            balances.append(balance)

        return balances

    def getAccountsTags(self):
        return self._requester.get_accounts_tags()

    def getHeight(self):

        r_data = self._requester.get_height()
        height = r_data.get('height')

        return height

    def getAddressBook(self):

        r_data = self._requester.get_address_book()
        address_book = r_data.get('entries')

        return address_book

    # TODO Somehow join out and in transfers
    def getOutTransfers(self):

        r_data = self._requester.get_out_transfers()

        transfers = r_data.get('out')

        out_transfers = []
        for t in transfers:

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

        r_data = self._requester.get_in_transfers()

        transfers = r_data.get('in')

        in_transfers = []

        for t in transfers:
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

            in_transfers.append(transfer)

        return in_transfers

    def heightToDate(self, height):

        moneroblocks_domain = "moneroblocks.info"
        block_header_path = "/api/get_block_header/%d" % height
        url = "https://%s%s" % (moneroblocks_domain, block_header_path)
        r = requests.get(url)
        r_data = r.json().get('block_header')

        timestamp = r_data.get('timestamp')

        if timestamp:
            localtime = time.localtime(timestamp)
            return time.strftime('%Y-%m-%d', localtime)
        else:
            raise Exception('Timestamp not found for height ' + height)
