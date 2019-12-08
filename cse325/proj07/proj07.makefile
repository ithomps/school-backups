#
# Usage:  make -f proj07.makefile
# Makes:  proj07
#

proj07: proj07.student.o
	g++ proj07.student.o -o proj07

proj07.student.o: proj07.student.c
	g++ -Wall -c proj07.student.c

clean:
	rm -f proj07.student.o
	rm -f proj07
