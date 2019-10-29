# tested in Python 3.6.4
import hashlib
import base64
import requests

with open("../../public_id", "r") as f:
    id_of_miner = f.read()

with open("../../prev_hash", "r") as f:
    hash_of_preceding_coin = f.read()

coin_name = "CPEN 442 Coin"
year = "2019"
coin_prefix = coin_name + year + hash_of_preceding_coin

coin_blob = 0
coin_string = coin_prefix + str(coin_blob) + id_of_miner

hashed = hashlib.md5(coin_string.encode())
hash_value = hashed.hexdigest()

while hash_value[0:8] != "00000000":
    coin_string = coin_prefix + str(coin_blob) + id_of_miner
    hashed = hashlib.md5(coin_string.encode())
    hash_value = hashed.hexdigest()
    coin_blob += 1

found_blob = coin_blob-1
coin_string = coin_prefix + str(found_blob) + id_of_miner
print(coin_string)