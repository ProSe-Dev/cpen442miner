import argparse
import random
import requests
import os 
import time

import signal
import subprocess
from multiprocessing import Event, Process, Manager

dir_path = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser(description='Let us do some mining')
parser.add_argument("--numWorkers", type=int, default=3, help="The private password")
parser.add_argument("mineCmd", default="go_miner.exe", help="Miner binary")
parser.add_argument("--offset", type=int, default=15459021544, help="Space between workers")
parser.add_argument("--idServer", help="Set an ID server to ping")
args = parser.parse_args()

with open("prev_hash", "rb") as prev_hash_file:
    hash_of_preceding_coin = prev_hash_file.read()
jobs = []
event = Event() # event for found desired hash
manager = Manager()
d = manager.dict()

def get_or_update_id(desired):
    resp = requests.get(args.idServer+"/id/%d" % desired)
    return int(resp.content)

if args.idServer is None:
    myId = 0
else:
    myId = get_or_update_id(0)
    print("Got ID: %d" % myId)

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

def f(event, i, d):
    """
    Helper for mining in a pool
    """
    cmd = args.mineCmd.split(" ")
    # probably won't be mining with more than 10 workers
    cmd.append(str(myId*args.offset*10 + i*args.offset))
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    d['pid%d' % i] = proc.pid
    (output, error) = proc.communicate()
    coin_blob = output.strip().decode('utf-8')
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
            args=(event, i, d,))
        p.start()
        jobs.append(p)
        print('created worker with PID:', p.pid)

def terminate_workers():
    """
    Helper for terminating workers
    """
    print("Terminating workers")
    print(d)
    for i, p in enumerate(jobs):
        p.terminate()
        pidid = "pid%d" % i
        if pidid in d:
            pid = d[pidid]
            if pid != -1:
                try:
                    os.kill(pid, signal.SIGINT)
                except:
                    pass # this will die if we found a coin blob
                d[pidid] = - 1
    jobs.clear()

def exec():
    while True:
        # if we found something, we can terminate all the
        # workers
        if event.is_set():
            terminate_workers()

        new_hash_of_preceding_coin = get_last_coin()
        if args.idServer is not None:
            get_or_update_id(myId)
        if new_hash_of_preceding_coin != hash_of_preceding_coin:
            hash_of_preceding_coin = new_hash_of_preceding_coin
            print("Head changed: %s" % hash_of_preceding_coin)
            with open("prev_hash", "wb") as prev_hash_file:
                prev_hash_file.write(hash_of_preceding_coin)
            terminate_workers()
            create_workers()
        elif not jobs:
            # reploy workers initally so we don't have to wait for next block
            print("Initalizing with head: %s" % hash_of_preceding_coin)
            create_workers()

        # wait 13 seconds
        # TODO: update the hashes in central server for even faster updates?
        time.sleep(13)

if __name__ == "__main__":
    exec()
