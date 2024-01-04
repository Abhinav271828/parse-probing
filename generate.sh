#!/bin/bash

# This is much slower than iterating in Haskell.
x="ab"
length=$1
for ((i = 0; i < $((2 ** $length)); i++)); do
    s=""
    n=$i
    for ((j = 0; j < $length; j++)); do
        s+=${x:$(($n % 2)):1}
        n=$(($n / 2))
    done
    ./generation $s g1
done
