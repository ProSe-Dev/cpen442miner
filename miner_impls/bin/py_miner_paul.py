import argparse
import base64
import hashlib
import math
import requests
import time

parser = argparse.ArgumentParser(description='Let us do some mining')
parser.add_argument("offset", type=int, default=7729510772, help="Space between workers")
args = parser.parse_args()

with open("public_id", "r") as f:
    id_of_miner = f.read().encode()

with open("prev_hash", "r") as f:
    hash_of_preceding_coin = f.read().encode()

def num_to_bytes(n):
    """
    Credits: https://stackoverflow.com/a/51446863
    """
    num_bytes = int(math.ceil(n.bit_length() / 8))
    n_bytes = n.to_bytes(num_bytes, byteorder='big')
    return n_bytes

def mine_coin(hash_of_preceding_coin, id_of_miner, offset=0):
    """
    Technically Python isn't ideal for performance intensive stuff like this,
    but proof of work here isn't too hard to compute.
    """
    coin_blob_ctr = offset
    while True:
        m = hashlib.md5()
        m.update(b"CPEN 442 Coin2019")
        m.update(hash_of_preceding_coin)
        coin_blob = num_to_bytes(coin_blob_ctr)
        m.update(coin_blob)
        m.update(id_of_miner)
        cpen442coin = m.hexdigest()
        if cpen442coin.startswith("00000000"):
            return cpen442coin, coin_blob_ctr, coin_blob, str(base64.b64encode(coin_blob), "utf-8")
        coin_blob_ctr += 1

cpen442coin, mined_coin_blob_ctr, _, mined_coin_blob_b64 = mine_coin(hash_of_preceding_coin, id_of_miner, args.offset)
print(mined_coin_blob_b64)
