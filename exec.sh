export NUM_WORKERS=${1:-3}
export ID_SERVER=${2:-}
chmod +x "$(pwd)/miner_impls/bin/go_impl"

python3 miner-control.py --numWorkers $NUM_WORKERS $([[ -n "$ID_SERVER" ]] && echo "--idServer $ID_SERVER") "$(pwd)/miner_impls/bin/go_impl"
