#!/bin/bash
#~/git/jline2/target/test-classes => run from here
curr_path=$(pwd)

#place asm-all jar in resources folder in jline2 folder
#add all the java class files to classpath
export CLASSPATH=.:/home/ms/git/jline2/resources/asm-all-5.0.3.jar:/home/ms/git/jline2/target/classes:.
javac asm/ASM_Example.java

for f in $(find jline -name '*class')
do
  mkdir -p /home/ms/git/jline2/ins/$(dirname $f)
  cd /home/ms/git/jline2/target/test-classes
  java asm.ASM_Example $curr_path/$f /home/ms/git/jline2/ins/$f
  cd ../../
done

echo "done"
