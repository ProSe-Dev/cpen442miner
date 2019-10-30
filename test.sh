export SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
export IMPL=${IMPL:-$1}

if [[ -z $IMPL ]]; then echo "Implementation must be specified" && exit 1; fi

pushd $SCRIPTPATH/test > /dev/null
"$SCRIPTPATH/miner_impls/bin/$IMPL" $(cat test_offset) || echo "Failed"
popd > /dev/null
