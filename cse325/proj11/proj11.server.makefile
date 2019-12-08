#
# Usage:  make -f proj11.server.makefile
# Makes:  proj11.server
#

proj11.server: proj11.server.c
	g++ proj11.server.c -o proj11.server

clean:
	rm -f proj11.server
