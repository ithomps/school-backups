#
# Usage:  make -f proj06
# Makes:  proj06
#

proj06: proj06.student.o
	g++ proj06.student.o -pthread -o proj06

proj06.student.o: proj06.student.c
	g++ -Wall -c proj06.student.c

clean:
	rm -f proj06.student.o
	rm -f proj06
