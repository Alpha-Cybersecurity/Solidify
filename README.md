# Solidify
Cryptocurrency Forensics

![doc/images/logos/logo2.png](doc/images/logos/logo2.png)

We use the word solidify as opposed to the term used to denominate the property that grants anonymity to monero: the fungibility.


## Install



## How does it work

1. Use monero-rpc to load the wallet

```
monero-wallet-rpc.exe --stagenet --password "admin" --rpc-bind-port 28088 --disable-rpc-login  --daemon-host monero-stagenet.exan.tech:38081  --wallet-file C:\Users\username\Documents\Monero\wallets\wallet/wallet
```
2. Use solidify to extract information

```
# For Gephi format
python solidify.py -a localhost -p 28088 -o monero.graphml

# For neo4j integration
python solidify.py -a localhost -p 28088 -nh localhost -np 7687 -nU neo4j -nP 1204
```

3. Visualize

Using [Gephi](https://gephi.org/) and the `.graphml` file:

![doc/images/gephiLoad.png](doc/images/gephiLoad.png)

Or with [neo4j](https://neo4j.com/):

![doc/images/neo4jLoad.png](doc/images/neo4jLoad.png)
