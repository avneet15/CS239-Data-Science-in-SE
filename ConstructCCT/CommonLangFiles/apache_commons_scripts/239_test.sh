#!/bin/bash
#~/git/commons-lang/target/classes => run from here
curr_path=$(pwd)

export CLASSPATH=.:/home/ms/git/commons-lang/resources/asm-all-5.0.3.jar:/home/ms/git/commons-lang/target/classes:.
javac asm/ASM_Example.java
echo "classpath is:"$CLASSPATH

#cd ../

for f in $(find org -name '*class')
#echo $f
do
  mkdir -p ins/$(dirname $f)
  cd /home/ms/git/commons-lang/target/test-classes
  java asm.ASM_Example $curr_path/$f /home/ms/git/commons-lang/ins/$f
  cd ../../
done

echo "done"
