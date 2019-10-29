export NUM_WORKERS=${1:-3}
export ID_SERVER=${2:-}
export DEFAULT_SERVER=${DEFAULT_SERVER:-http://104.42.36.58:5000}
chmod +x "$(pwd)/miner_impls/bin/go_impl"

python3 miner-control.py --numWorkers $NUM_WORKERS $([[ -n "$ID_SERVER" ]] && echo "--idServer $ID_SERVER") $([[ -n "$USE_DEFAULT_SERVER" ]] && echo "--idServer $DEFAULT_SERVER") "$(pwd)/miner_impls/bin/go_impl"

