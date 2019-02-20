import requests

class MoneroRPC:

    # monero-wallet-rpc.exe --stagenet --password "" --rpc-bind-port 28088 --disable-rpc-login  --daemon-host monero-stagenet.exan.tech:38081  --wallet-dir C:\Users\carlos\Documents\Monero\wallets\carlos-stagenet
    #TODO 
    #init method and start monero-wallet-rpc

    def getAddress(self):

        headers = {
        'Content-Type': 'application/json',
        }

        data = '{"jsonrpc":"2.0","id":"0","method":"get_address","params":{"account_index":0}}'

        response = requests.post('http://127.0.0.1:28088/json_rpc', headers=headers, data=data)

        return response.json()['result']

    def getOutTransfers(self):

        headers = {
            'Content-Type': 'application/json',
        }

        data = '{"jsonrpc":"2.0","id":"0","method":"get_transfers","params":{"out":true}}'

        response = requests.post('http://127.0.0.1:28088/json_rpc', headers=headers, data=data)

        return response.json()['result']['out']

    def getInTransfers(self):

        headers = {
            'Content-Type': 'application/json',
        }

        data = '{"jsonrpc":"2.0","id":"0","method":"get_transfers","params":{"in":true}}'

        response = requests.post('http://127.0.0.1:28088/json_rpc', headers=headers, data=data)

        return response.json()['result']['in']







moneroRPC = MoneroRPC()

moneroRPC.getAddress()
