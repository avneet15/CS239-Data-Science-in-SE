#!/bin/bash
#~/git/jline2 => run from here
curr_path=$(pwd)

export CLASSPATH=.:/home/ms/git/jline2/lib/*:.

cd /home/ms/git/jline2/ins

for f in $(find . -name '*Test*.class')
do
  #echo $f
  name="$(echo $f | tr / .)"
  name=${name:2:- 6}
  echo $name
  java org.junit.runner.JUnitCore $name >> ../jline_stackTrace.txt 2>&1
done

echo "done"

#export CLASSPATH=.:/home/ms/git/jline2/lib/junit-4.12.jar:/home/ms/git/jline2/lib/easymock-3.3.1.jar:/home/ms/git/jline2/lib/hamcrest-all-1.3.jar:/home/ms/git/jline2/lib/hamcrest-core-1.3.jar:/home/ms/git/jline2/lib/objenesis-2.1.jar:/home/ms/git/jline2/lib/cglib-3.1.jar:/home/ms/git/jline2/lib/cglib-nodep-2.2.2.jar:/home/ms/git/jline2/lib/jansi-1.11.jar:/home/ms/git/jline2/lib/javassist-3.19.0-GA.jar:/home/ms/git/jline2/lib/powermock-api-easymock-1.6.2.jar:/home/ms/git/jline2/lib/powermock-api-support-1.6.2.jar:/home/ms/git/jline2/lib/powermock-core-1.6.2.jar:/home/ms/git/jline2/lib/powermock-module-junit4-1.6.2.jar:/home/ms/git/jline2/lib/powermock-module-junit4-common-1.6.2.jar:/home/ms/git/jline2/lib/powermock-reflect-1.6.2.jar.
