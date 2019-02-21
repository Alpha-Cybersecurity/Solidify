import requests
import random
import subprocess
import time
import signal

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
        signal.signal(signal.SIGBUS, self.end)
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

        return response.json()['result']

    def getBalance(self):

        headers = {
        'Content-Type': 'application/json',
        }

        data = '{"jsonrpc":"2.0","id":"0","method":"get_balance","params":{"account_index":0,"address_indices":[0,1]}}'

        response = requests.post(self.json_rpc_address, headers=headers, data=data)

        return response.json()['result']

    def getHeight(self):

        headers = {
        'Content-Type': 'application/json',
        }

        data = '{"jsonrpc":"2.0","id":"0","method":"get_height"}'

        response = requests.post(self.json_rpc_address, headers=headers, data=data)

        return response.json()['result']

    def getOutTransfers(self):

        headers = {
            'Content-Type': 'application/json',
        }

        data = '{"jsonrpc":"2.0","id":"0","method":"get_transfers","params":{"out":true}}'

        response = requests.post(self.json_rpc_address, headers=headers, data=data)

        return response.json()['result']['out']

    def getInTransfers(self):

        headers = {
            'Content-Type': 'application/json',
        }

        data = '{"jsonrpc":"2.0","id":"0","method":"get_transfers","params":{"in":true}}'

        response = requests.post(self.json_rpc_address, headers=headers, data=data)

        return response.json()['result']['in']







#
# #
# moneroRPC = MoneroRPC('C:\\Users\\carlos\\Documents\\Monero\\wallets\\carlos-stagenet\\carlos-stagenet')
#
# print(moneroRPC.getHeight())
