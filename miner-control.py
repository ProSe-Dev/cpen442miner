import argparse
import random
import requests
import os 
import time

from subprocess import check_output
from multiprocessing import Event, Process

dir_path = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser(description='Let us do some mining')
parser.add_argument("--numWorkers", type=int, default=3, help="The private password")
parser.add_argument("mineCmd", default="go_miner.exe", help="Miner binary")
parser.add_argument("--offset", type=int, default=random.randrange(7729510772,15459021544,1), help="Space between workers")
args = parser.parse_args()

with open("prev_hash", "rb") as prev_hash_file:
    hash_of_preceding_coin = prev_hash_file.read()
jobs = []
event = Event() # event for found desired hash

with open("public_id", "r") as public_id_file:
    id_of_miner = public_id_file.read()
    print("Mining using public ID: %s" % id_of_miner)

def get_last_coin():
    """
    Ping the server to get the last coin ID
    """
    resp = requests.post("http://cpen442coin.ece.ubc.ca/last_coin")
    if resp.status_code != 200 or "coin_id" not in resp.json():
        raise Exception("Couldn't get last coin")
    return resp.json()["coin_id"].encode()

def claim_coin_blob(coin_blob):
    data = {
        "coin_blob": coin_blob,
        "id_of_miner": id_of_miner, 
    }
    print("Submitting: %s" % data)
    return requests.post("http://cpen442coin.ece.ubc.ca/claim_coin", json=data)

def f(event, i):
    """
    Helper for mining in a pool
    """
    cmd = args.mineCmd.split(" ")
    cmd.append(str(i*args.offset))
    coin_blob = check_output(cmd).strip()
    print("COIN BLOB: %s" % coin_blob)
    resp = claim_coin_blob(coin_blob)
    if resp.status_code == 200:
        print("Yay, found a coin!!")
    event.set()

def create_workers():
    """
    Helper for creating workers
    """
    print("Creating workers")
    for i in range(args.numWorkers):
        p = Process(
            target=f,
            args=(event, i,))
        p.start()
        jobs.append(p)

def terminate_workers():
    """
    Helper for terminating workers
    """
    print("Terminating workers")
    for p in jobs:
        p.terminate()
    jobs.clear()

while True:
    # if we found something, we can terminate all the
    # workers
    if event.is_set():
        terminate_workers()

    new_hash_of_preceding_coin = get_last_coin()
    if new_hash_of_preceding_coin != hash_of_preceding_coin:
        hash_of_preceding_coin = new_hash_of_preceding_coin
        print("Head changed: %s" % hash_of_preceding_coin)
        with open("prev_hash", "wb") as prev_hash_file:
            prev_hash_file.write(hash_of_preceding_coin)
        terminate_workers()
        create_workers()

    # wait 30 seconds
    time.sleep(30)
