#!/bin/sh
# ./sweep.sh BMAX FEATURES...   for each feature string: largest bound B <= BMAX at which ./types works, and the type count there
BMAX=$1; shift
for f in "$@"; do
  last=0; nt=0
  for b in $(seq 2 $BMAX); do
    r=$(${TYPES:-./types} $b "$f" | tail -1)
    case "$r" in *WORKS) last=$b; nt=$(echo "$r" | sed 's/.*types \([0-9]*\),.*/\1/');; *) break;; esac
  done
  echo "'$f': works through B = $last ($nt types)$( [ $last = $BMAX ] && echo ' (not run further)' )"
done
