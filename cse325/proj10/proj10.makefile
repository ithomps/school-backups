#
# Usage:  make -f proj10.makefile
# Makes:  proj10
#

proj10: proj10.student.o
	g++ proj10.student.o -o proj10

proj10.student.o: proj10.student.c
	g++ -Wall -c proj10.student.c

clean:
	rm -f proj10.student.o
	rm -f proj10
