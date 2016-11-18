import os

files = os.listdir()

for f in files:
    if f.endswith('.hlt'):
        os.remove(f)