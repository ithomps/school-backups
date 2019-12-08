#
# Usage:  make -f proj11.client.makefile
# Makes:  proj11.client
#

proj11.client: proj11.client.c
	g++ proj11.client.c -o proj11.client

clean:
	rm -f proj11.client
