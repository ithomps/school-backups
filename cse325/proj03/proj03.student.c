/**
 * \file proj03.student.c
 *
 * \author Ian Thompson
 */

using namespace std;

#include <iostream>
#include <cstring>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>



// \param argc Number of arguments
// \param argv Array of arguments
int main(int argc, char *argv[])
{
  // Default values of file modifiers
  int inputBufferSize = 256;
  bool mod = false;
  bool append = false;
  char * source;
  char * des;
  int files = 0;

  // For loop to parse command line
  for (int i=1; i<argc; i++)
  {

    if ((argv[i])[0] == '-')    // First char is a '-'
    {
      if ((argv[i])[1] == 'b' )
      {
        inputBufferSize = atoi(argv[i+1]);
        inputBufferSize = 2 << (inputBufferSize - 1);   // Left shift for powers of two
        i += 1;   // Skip number next time through loop
      }
      else if ((argv[i])[1] == 'm' )
      {
        mod = true; // Destination file can be modified
      }
      else if ((argv[i])[1] == 't' )
      {
        append = false;   // Detination file will not ne truncated
      }
      else if (((argv[i])[1] == 'n') && ((argv[i])[2] == 'm'))
      {
        mod = false;    // Destination file can't be modfied
      }
      else if (((argv[i])[1] == 'n') && ((argv[i])[2] == 't'))
      {
        append = true;    // Destination file can be truncated
      }
      else
      {
        printf("%s\n", "Invalid tag entered.");
        exit(0);
      }
    } // end if

    else  // Argument is a file
    {
      if (files == 0)
      {
        int size = strlen(argv[i]);
        source = (char*) malloc (size+1);   // Allot space for source file
        strcpy(source, argv[i]);    // Save filepath
        files++;
      }
      else if (files == 1)
      {
        int size = strlen(argv[i]);
        des = (char*) malloc (size+1);    // Allot space for destination file
        strcpy(des, argv[i]);   // Save filepath
        files++;
      }
      else
      {
        printf("%s\n", "Only Enter Two files");
        exit(0);
      }
    } // end else

  } // end for

  // Open source file
  int storage_size = inputBufferSize;   // Buffer for input file
  char * storeInput = (char*) malloc (storage_size+1);

  int fd_sc = open(source, O_RDONLY, S_IRUSR);  // Open source file read only

  // Test for errors
  if (fd_sc == -1)
  {
    printf("%s\n", "Error opening file");
    exit(0);
  }
  // Read input file
  size_t buf_size = read( fd_sc, &storeInput, inputBufferSize);   // Read into buffer

  // Open destination file
  if (mod)
  {
    if (append) // Add all to end of file
    {
      int fd_des = open(des, O_APPEND, S_IWUSR);
      write(fd_des, &storeInput, buf_size);
    }
    else // Replace existing file
    {
      int fd_des = open(des, O_CREAT, S_IWUSR);
      write(fd_des, &storeInput, buf_size);
    }
  } // end if
  else  // Do not modify
  {
    int fd_des = open(des, O_CREAT | O_EXCL, S_IWUSR);  // Only write to new file
    write(fd_des, &storeInput, buf_size);
  }

  free(des);
  free(source);
  free (storeInput);
}
