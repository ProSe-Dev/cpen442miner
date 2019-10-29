import argparse
import requests
import time

from subprocess import check_output
from multiprocessing import Event, Process

parser = argparse.ArgumentParser(description='Let us do some mining')
parser.add_argument("--numWorkers", type=int, default=3, help="The private password")
parser.add_argument("miner", default="go_miner.exe", help="Miner binary")
parser.add_argument("--offset", type=int, default=7729510772, help="Space between workers")
args = parser.parse_args()

hash_of_preceding_coin = b"2e3a8e88a060cedcd9ac7b74fadd58e0"
jobs = []
event = Event() # event for found desired hash

with open("public_id", "r") as f:
    id_of_miner = f.read()

def get_last_coin():
    """
    Ping the server to get the last coin ID
    """
    resp = requests.get("http://cpen442coin.ece.ubc.ca/last_coin")
    if resp.status_code != 200 or "coin_id" not in resp.json():
        raise Exception("Couldn't get last coin")
    return resp.json()["coin_id"].encode()

def claim_coin_blob(coin_blob):
    data = {
        "coin_blob": coin_blob,
        "id_of_miner": id_of_miner, 
    }
    return requests.post("http://cpen442coin.ece.ubc.ca/claim_coin", json=data)

def f(event, i):
    """
    Helper for mining in a pool
    """
    coin_blob = subprocess.check_output([args.miner])
    claim_coin_blob(coin_blob)
    event.set()
    print("event set")

def create_workers(miner_id):
    """
    Helper for creating workers
    """
    print("Creating workers")
    for i in range(num_workers):
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
        print("Quitting")
        break
    # this section is for if we want to get a valid coin
    # for fun; ping the last coin endpoint once every
    # minute and if the hash has changed then we restart
    # the workers
    new_hash_of_preceding_coin = get_last_coin()
    if new_hash_of_preceding_coin != hash_of_preceding_coin:
        hash_of_preceding_coin = new_hash_of_preceding_coin
        print("Head changed: %s" % hash_of_preceding_coin)
        with open("prev_hash", "w") as f:
            f.write(hash_of_preceding_coin)
        terminate_workers()
        create_workers(miner_id)

    # wait 60 seconds
    time.sleep(60)