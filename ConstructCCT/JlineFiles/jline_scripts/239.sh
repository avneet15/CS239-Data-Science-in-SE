#!/bin/bash

curr_path=$(pwd)

export CLASSPATH=.:/home/ms/git/jline2/resources/asm-all-5.0.3.jar:.
javac asm/ASM_Example.java
echo "classpath is:"$CLASSPATH


for f in $(find jline -name '*class')
#echo $f
do
  mkdir -p /home/ms/git/jline2/ins/$(dirname $f)
  cd /home/ms/git/jline2/target/classes
  java asm.ASM_Example  $curr_path/$f /home/ms/git/jline2/ins/$f
  cd ../../
done

echo "done"

