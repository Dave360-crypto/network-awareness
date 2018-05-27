"""
import sys
import time

for i in range(100):
    sys.stdout.write("\r{0}>".format("="*i))
    sys.stdout.flush()
    time.sleep(0.05)
"""