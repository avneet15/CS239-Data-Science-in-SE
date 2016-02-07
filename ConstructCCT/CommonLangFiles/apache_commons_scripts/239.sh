#!/bin/bash

curr_path=$(pwd)

export CLASSPATH=.:$curr_path/../../../resources/asm-all-5.0.3.jar:.
javac /asm/ASM_Example.java
echo "classpath is:"$CLASSPATH

cd /home/ms/git/commons-lang/target/

for f in $(find org/apache/commons/lang3 -name '*class')
#echo $f
do
  mkdir -p java/instrumented/$(dirname $f)
  cd /home/ms/git/commons-lang/target/classes
  java asm.ASM_Example /$f $curr_path/../instrumented/$f
  cd ../../
done

echo "done"

