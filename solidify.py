from moneroRpcClass import MoneroRPC
import argparse
import random
from draw import generate_draw, insert_neo4j

from entities import Wallet

import logging
log = logging.getLogger(__name__)

def main(host, port, wallet_file, exe, output, neo4j):
    mrpc = MoneroRPC(host, port, wallet_file=wallet_file, exe=exe)
    w = Wallet(mrpc)
    generate_draw(w, output)
    if neo4j.get('neoHost'):
        insert_neo4j(w, neo4j.get('neoHost'), neo4j.get('neoPort'),neo4j.get('neoUser'), neo4j.get('neoPass'))

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Solidify')
    parser.add_argument('-f', '--wallet-file', dest='wallet_file', help='Path to wallet file')
    parser.add_argument('-x', '--client-executable', dest='x', help='Path to RPC client')
    parser.add_argument('-a', '--client-host', dest='host', help='Running RPC client host')
    parser.add_argument('-p', '--client-port', dest='port', type=int, help='Running RPC client port')
    parser.add_argument('-nh', '--neoHost', dest='neoHost', help='Neo4j host')
    parser.add_argument('-np', '--neoPort', dest='neoPort', help='Neo4j Port')
    parser.add_argument('-nU', '--neoUser', dest='neoUser', help='Neo4j User')
    parser.add_argument('-nP', '--neoPassword', dest='neoPassword', help='Neo4j Password')
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

    neo4j = {}
    if args.neoHost: 
        neo4j['neoHost'] = args.neoHost
        neo4j['neoPort'] = args.neoPort
        neo4j['neoUser'] = args.neoUser
        neo4j['neoPass'] = args.neoPassword

    main(host, port, wallet_file, exe, output, neo4j)
