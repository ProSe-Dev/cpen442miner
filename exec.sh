export NUM_WORKERS=${1:-3}
chmod +x "$(pwd)/miner_impls/bin/go_impl"

python3 miner-control.py --numWorkers $NUM_WORKERS "$(pwd)/miner_impls/bin/go_impl"
