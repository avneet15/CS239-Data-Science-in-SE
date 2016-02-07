#!/bin/bash
#~/git/commons-lang/target/classes => run from here
curr_path=$(pwd)

export CLASSPATH=.:/home/ms/git/commons-lang/lib/junit-4.12.jar:/home/ms/git/commons-lang/lib/commons-io-2.4.jar:/home/ms/git/commons-lang/lib/easymock-3.4.jar:/home/ms/git/commons-lang/lib/hamcrest-all-1.3.jar:/home/ms/git/commons-lang/lib/hamcrest-core-1.3.jar:/home/ms/git/commons-lang/lib/objenesis-2.2.jar:.

cd /home/ms/git/commons-lang/ins
#cd ../

for f in $(find . -name '*Test*.class')
do
  #echo $f
  name="$(echo $f | tr / .)"
  name=${name:2:- 6}
  echo $name
  java org.junit.runner.JUnitCore $name >> ../apache_stack.txt 2>&1
done

echo "done"

#java -cp .:/home/ms/git/commons-lang/lib/junit-4.12.jar:/home/ms/git/commons-lang/lib/commons-io-2.4.jar:/home/ms/git/commons-lang/lib/easymock-3.4.jar:/home/ms/git/commons-lang/lib/hamcrest-all-1.3.jar:/home/ms/git/commons-lang/lib/hamcrest-core-1.3.jar:/home/ms/git/commons-lang/lib/objenesis-2.2.jar org.junit.runner.JUnitCore org.apache.commons.lang3.SystemUtilsTest >> ../okay.txt 2>&1
# above line is executed in /git/commons-lang/ins
