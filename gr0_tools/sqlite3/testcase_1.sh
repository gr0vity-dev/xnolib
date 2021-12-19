#!/bin/bash
#run testcase_1.sh {your_seed}
#Example:
#run testcase_1.sh 0000000000000000000000000000000000000000000000000000000000000000
#Make sure that all accounts for your selected seed have funds from index 1 to 5001

seed=$1
cd ../../ && \
python3 gr0_conf_duration_tester.py --start_index=1 --accs=1000 --tx_per_acc=5 --tps=50 --amount_raw=1 --rpc_process=true --source_seed=$seed --tx_wait=1 --block_type=1 && \
python3 gr0_conf_duration_tester.py --start_index=1 --accs=5000 --tx_per_acc=1 --tps=50 --amount_raw=1 --rpc_process=true --source_seed=$seed --tx_wait=1 --block_type=1 && \
python3 gr0_conf_duration_tester.py --start_index=1 --accs=1000 --tx_per_acc=5 --tps=50 --amount_raw=1 --rpc_process=true --source_seed=$seed --tx_wait=1 --block_type=1 && \
python3 gr0_conf_duration_tester.py --start_index=1 --accs=5000 --tx_per_acc=1 --tps=50 --amount_raw=1 --rpc_process=true --source_seed=$seed --tx_wait=1 --block_type=1 && \
for i in {1..21}; do python3 gr0_conf_duration_tester.py --start_index=1 --accs=2 --tx_per_acc=2 --tps=2 --amount_raw=1 --rpc_process=true --source_seed=$seed --tx_wait=1 --block_type=2 ; done &&
cd gr0_tools/sqlite3/ && \
python3 select.py --limit=25
