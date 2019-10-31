import daemon

import miner_control

with daemon.DaemonContext():
    miner_control.exec()

