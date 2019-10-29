import time

from subprocess import check_output

run_args = [("go", "../miner_impls/bin/go_impl"), ("python", "python3 ../miner_impls/bin/py_miner_paul.py")]

with open("expected_offset", "r") as f:
    offset = int(f.read())

for name, r in run_args:
    start = time.time()
    cmd = r.split(" ")
    cmd.append(str((offset//1000)*999))
    print(cmd)
    coin_blob = check_output(cmd).strip()
    end = time.time()
    elapsed = end - start
    print("Found coin in %.2f seconds\nCoin blob: %s" % (elapsed, coin_blob))
    with open("times/%s" % name, "w") as f:
        f.write("Coin: %s Time: %.2fs" % (coin_blob, elapsed))
