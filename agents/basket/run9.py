import sys
from basket2 import run
allw = len(sys.argv)>1
out = run(int(sys.argv[2]) if len(sys.argv)>2 else 9, loose=True, allw=allw, verbose=True)
