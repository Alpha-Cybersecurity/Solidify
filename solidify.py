from moneroRpcClass import MoneroRPC
import argparse
import random
from draw import generate_draw, insert_neo4j

from entities import Wallet

import logging
log = logging.getLogger(__name__)

def main(host, port, wallet_file, exe, output):
    mrpc = MoneroRPC(host, port, wallet_file=wallet_file, exe=exe)
    w = Wallet(mrpc)
    #generate_draw(w, output)
    insert_neo4j(w, "localhost", "7687","neo4j", "1204")

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Solidify')
    parser.add_argument('-f', '--wallet-file', dest='wallet_file', help='Path to wallet file')
    parser.add_argument('-x', '--client-executable', dest='x', help='Path to RPC client')
    parser.add_argument('-a', '--client-host', dest='host', help='Running RPC client host')
    parser.add_argument('-p', '--client-port', dest='port', type=int, help='Running RPC client port')
    parser.add_argument('-o', '--output', dest='output', help='Output filename')

    args = parser.parse_args()

    if not args.x:
        if not args.host:
            log.error("You must specify host if there is not a running instance")
            exit(-1)
        if args.wallet_file:
            log.error("Mustn't specify wallet file if not launching new RPC instance")
            exit(-1)
        exe = None
        wallet_file = None
    else:

        if not args.wallet_file:
            log.error("Must specify wallet file")
            exit(-1)

        exe = args.x # "C:\\Users\\carlos\\Desktop\\monero-gui-v0.13.0.4\\monero-wallet-rpc.exe"
        wallet_file = args.wallet_file

    if args.host:
        if not args.port:
            log.error("If you specify host, you must specity port")
            exit(-1)
        if args.x:
            log.error("You mustn't specify host if you want a new RPC instance")
            exit(-1)

    host = args.host if args.host else "127.0.0.1"
    port = args.port if args.port else random.randint(10240, 65000)
    output = args.output if args.output else "monero.graphml"

    main(host, port, wallet_file, exe, output)
