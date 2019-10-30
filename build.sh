export SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
export DIRS=$(ls -d $SCRIPTPATH/miner_impls/*/)
for dir in $DIRS
do
  if [[ $(basename $dir) != "bin" ]]; then pushd $dir > /dev/null && ./build.sh && popd > /dev/null
  fi
done

