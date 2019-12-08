/**
 * \file proj11.server.c
 *
 * \author Ian Thompson
 *
 * Server to transfer files in response to client commands
 */


#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netdb.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <fcntl.h>

#define BSIZE 256

/**
 * Process get command from client and send requested file
 * \param argc Number of arguments to the server
 * \param argv Array of command line inputs
 */
int main(int argc, char* argv[])
{
  // Create server socket
  int listen_sd = socket( AF_INET, SOCK_STREAM, 0 );
  if (listen_sd < 0)
  {
    perror( "socket" );
    exit( 2 );
  }

  // Create server address structure
  struct sockaddr_in saddr;

  bzero( &saddr, sizeof(saddr) );
  saddr.sin_family = AF_INET;
  saddr.sin_addr.s_addr = htonl( INADDR_ANY );
  saddr.sin_port = htons( 0 );

  // Bind server
  int bstat = bind( listen_sd, (struct sockaddr *) &saddr, sizeof(saddr) );
  if (bstat < 0)
  {
    perror( "bind" );
    exit( 3 );
  }

  // Get port this host is operating on
  socklen_t len = sizeof(saddr);
  int sockName = getsockname( listen_sd, (struct sockaddr *) &saddr, &len ) ;

  // Get the domain name for this host
  char hostname[256];
  gethostname( hostname, 256 );


  // Display domain and port number
  printf( "%s", hostname );
  printf( " %d\n", ntohs( saddr.sin_port ) );

  // Listen on a free port
  int lstat = listen( listen_sd, 5 );
  if (lstat < 0)
  {
    perror( "listen" );
    exit( 4 );
  }

  // Addresses for client socket
  struct sockaddr_in caddr;
  unsigned int clen = sizeof(caddr);

  // Accept connection to client
  int comm_sd = accept( listen_sd, (struct sockaddr *) &caddr, &clen );
  if (comm_sd < 0)
  {
    perror( "accept" );
    exit( 5 );
  }

  char buffer[BSIZE];
  char quit[BSIZE] = "quit";
  char line[BSIZE];
  char fileStart[BSIZE] = "-start file-";
  char fileEnd[BSIZE] = "-end file-";
  char* status;

  // Wait for messages from client
  while (1)
  {
    // Recieve command from client process
    bzero( buffer, BSIZE );
    int nrecv = recv( comm_sd, buffer, BSIZE, 0 );
    if (nrecv < 0)
    {
      perror( "recv" );
      exit( 8 );
    }

    // Process input from client
    if (strncmp(buffer, quit, 4) == 0)    // Quit command
    {
      close( comm_sd );
      exit(1);
    }

    // Open file from client command
    FILE *fp;
    char block[255];
    fp = fopen(buffer, "r");
    bool endOfFile = false;

    // Send start of file flag
    if (fp > 0)
    {
      int messageStart = send( comm_sd, fileStart, strlen(fileStart), 0 );
      if (messageStart < 0)
      {
        perror( "send" );
        exit( 9 );
      }
    }

    int sendLine;

    // Loop through file
    while (!endOfFile)
    {
      // Read file line by line
      status = NULL;
      status = fgets(block, 255, fp);

      // Check new line is still valid
      if (status != NULL)
      {
        // Send line to client
        sendLine = send( comm_sd, block, strlen(block), 0 );
        if (sendLine < 0)
        {
          perror( "send" );
          exit( 9 );
        }

      }
      else
      {
        endOfFile = true;
      }

    }

    int messageEnd = send( comm_sd, fileEnd, strlen(fileEnd), 0 );
    if (messageEnd < 0)
    {
      perror( "send" );
      exit( 9 );
    }

    close( comm_sd );

  }

}
