/**
 * \file proj11.client.c
 *
 * \author Ian Thompson
 *
 * A client program to get input from the user
 * and communicate that with the server.
 */

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <netdb.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define BSIZE 256


/**
 * Connect to remote server and recieve requested file
 * \param argc Number of arguments to the server
 * \param argv Array of command line inputs
 */
int main(int argc, char* argv[])
{
  // Error check command line input
  if (argc != 3)
  {
    printf( "Usage: %s <host> <port>\n", argv[0] );
    exit( 1 );
  }

  // Extract domain and port
  char * hostname = argv[1];
  int port = atoi( argv[2] );

  // Create socket
  int sd = socket( AF_INET, SOCK_STREAM, 0 );
  if (sd < 0)
  {
    perror( "socket" );
    exit( 2 );
  }

  struct hostent * server = gethostbyname( hostname );
  if (server == NULL)
  {
    printf( "Error: no such host %s\n", hostname );
    exit( 3 );
  }

  // Create address structure
  struct sockaddr_in saddr;

  bzero( &saddr, sizeof(saddr) );
  saddr.sin_family = AF_INET;
  bcopy( server->h_addr, &saddr.sin_addr.s_addr, server->h_length );
  saddr.sin_port = htons( port );

  // Connct to server
  int stat = connect( sd, (struct sockaddr *) &saddr, sizeof(saddr) );
  if (stat < 0)
  {
    perror( "connect" );
    exit( 4 );
  }


  // String for processing input
  char buffer[BSIZE];
  char quit[BSIZE] = "quit";
  char get[BSIZE] = "get";
  char fileStart[BSIZE] = "-start file-";
  char fileEnd[BSIZE] = "-end file-";

  // Accept commands from user
  while (1)
  {
    // Store user inpt in buffer
    printf( "Enter command or quit to exit: ");
    bzero( buffer, BSIZE );
    fgets( buffer, BSIZE, stdin );

    // Echo back output
    printf("%s\n", buffer);

    // Enter quit to exit
    if (strncmp(buffer, quit, 4) == 0)
    {
      // Send server quit message
      int nsend = send( sd, quit, strlen(quit), 0 );
      if (nsend < 0)
      {
        perror( "send" );
        exit( 5 );
      }

      // Close client socket
      close( sd );
      exit(1);
    }
    else if (strncmp(buffer, get, 3) == 0)  // Get command
    {
      // Parse command into files
      const char whitespace[2] = " ";
      char *remotefile;
      char *localfile;
      char *file;

      // Remove command before first file
      file = strtok(buffer, whitespace);

      // Extract first file
      remotefile = strtok(NULL, whitespace);

      // Extract second file
      localfile = strtok(NULL, whitespace);

      // Trim newline from filenme
      strtok(localfile, "\n");


      // Error checking for get command
      if (NULL == localfile || NULL == remotefile)
      {
        printf("Get command requires two files.\n");
      }
      else
      {
        // Request server for specified file
        int nsend = send( sd, remotefile, strlen(remotefile), 0 );
        if (nsend < 0)
        {
          perror( "send" );
          exit( 5 );
        }

        // Open localfile
        FILE *fp;
        fp = fopen(localfile, "w");
        bool acceptingMessages = false;

        // Check file opened proporly
        if (fp == NULL)
        {
          printf("Error opening localfile\n");

          // Close client socket
          close( sd );
          exit(1);
        }

        // Recieve start of file message
        int nrecv = recv( sd, buffer, BSIZE, 0 );
        if (nrecv < 0)
        {
          perror( "recv" );
          exit( 4 );
        }

        if (strncmp(buffer, fileStart, 12) == 0)
        {
          // Begin listening for file
          acceptingMessages = true;
        }

        int serverMessage = 0;

        // Loop listening for server messages
        while (acceptingMessages)
        {
          // Recieve message
          bzero( buffer, BSIZE );
          serverMessage = recv( sd, buffer, BSIZE, 0 );
          if (serverMessage < 0)
          {
            perror( "recv" );
            exit( 4 );
          }

          // Check for end flag
          if (strncmp(buffer, fileEnd, 12) == 0)
          {
            acceptingMessages = false;

            // Send server quit message
            int nsend = send( sd, quit, strlen(quit), 0 );
            if (nsend < 0)
            {
              perror( "send" );
              exit( 5 );
            }

            // Close client socket
            close( sd );
            exit(1);

          }
          else    // PLace line into local file
          {
            fputs(buffer, fp);
          }

        }   // end listening loop

      }

    }   // end get command processing
    else
    {
      printf("Invalid command: %s\n", buffer);
    }

  }
}
