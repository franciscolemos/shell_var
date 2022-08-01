import subprocess
import time
for train_test_split in range(60, 96, 5):
    print(train_test_split)
    process = subprocess.Popen(["./auto.sh", str(train_test_split)])
    time.sleep(10)
