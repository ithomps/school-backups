/**
 * \file proj06.student.case
 * \author Ian Thompson
 * Implements a banking system using
 * producers and consumers
 */

#include <stdio.h>
#include <unistd.h>
#include <semaphore.h>
#include <pthread.h>
#include <string>
#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>

using namespace std;

// Struct to describe a buffer slot
struct item
{
     int accNum;
     int type;    // 0: Deposit, 1: Withdrawl
     double ammount;
     int prodNum;
};

void * read_transactions( void * arg );
void * write_transactions( void * arg );

// Semaphores to protect buffer
sem_t S;
sem_t N;
sem_t E;

// Semaphore to protcect ActiveThreads
sem_t lock;

// Buffer declared to maximum size, indexed with mod trueSize
struct item boundedBuffer[20];

// Vector to save account information
vector<pair<int,double>> accountInfo;

int UsableBufferSize = 5;   // Usable slots in circular buffer
int BufferIn = 0;           // Slot for producers
int BufferOut = 0;          // SLot for consumers
int ActiveThreads = 1;      // Number of running producers

/**
 * Implement banking system
 * \param argc Number of arguments
 * \param argv Array of arguments
 */
int main(int argc, char *argv[])
{
  int numProducers = 1;   // Default value of producers
  int bufferSize = 5;     // Default buffer size

  int input;            // Integer to parse command line values
  char *strtolPtr;      // Pointer used by strtol function

  // For loop to parse command line
  for (int i=1; i<argc; i++)
  {

    if (argv[i][0] == '-')
    {
      if (argv[i][1] == 'p')
      {
        input = strtol(argv[i+1], &strtolPtr, 10);  // Edit number of producers

        if (input < 11)
        {
          numProducers = input;   // Producers cannot exeed 10
        }

      }
      else if (argv[i][1] == 'b')
      {
        input = strtol(argv[i+1], &strtolPtr, 10);  // Edit buffer size

        if (input < 21)
        {
          bufferSize = input;   // Buffer size cannot exceed 20
        }
      }
    }

  }

  /**
    Process accouts.old
   */

   char *strPtr;      // Pointer used by strtol function
   string::size_type sz;
   int num;              // Variables to store values from accounts.old
   double balance;

   string filename = "accounts.old";
   ifstream r_file;
   string line;

   r_file.open(filename);

   while (r_file >> line)
   {
     const char * aNum = line.c_str();
     num = strtol(aNum, &strPtr, 10);

     r_file >> line;
     string::size_type sz;
     balance = stod(line, &sz);

     // Add input info to vector
     accountInfo.push_back(std::make_pair(num, balance));
   }

   UsableBufferSize = bufferSize;   // Save input size to buffer

   ActiveThreads = numProducers;    // Numuber of running producers

  // Initialize producer and consumer threads
  pthread_t producerThread[numProducers];
  pthread_t consumerThread;

  // Buffer semaphores
  sem_init( &S, 0, 1 );
  sem_init( &N, 0, 0 );
  sem_init( &E, 0, bufferSize );

  // Active Threads semaphore
  sem_init( &lock, 0, 1 );

  // Start consumer thread
  if (pthread_create (&consumerThread, NULL, write_transactions, NULL))
  {
    printf( "*** Error creating thread ***\n" );
    exit( -1 );
  }

  for (int i=0; i<numProducers; i++)
  {
    // Edit filename to send to threads
    string fileName = "transN";
    string num = to_string(i);
    fileName.at(5) = num.at(0);   // transN where N is the thread number

    // Pass edited filename and start producer thread
    if (pthread_create( &producerThread[i], NULL, read_transactions, &fileName))
    {
      printf( "*** Error creating thread ***\n" );
      exit( -1 );
    }

  }
  for (int i=0; i<numProducers; i++)
  {
    if (pthread_join( producerThread[i], NULL ))
    {
      printf( "*** Error joining thread ***\n" );
      exit( -2 );
    }
  }

}

void * read_transactions( void * file )
{
  // Variables to save to a slot in buffer
  int accountNum;
  int type;
  int ammount;

  int input;            // Integer to parse file values
  char *strtolPtr;      // Pointer used by strtol function

  string filename = *static_cast<string*>(file);
  ifstream r_file;
  string line;

  char producerNum = filename.at(5);
  int pNum = producerNum - '0';

  r_file.open(filename);

  while (r_file >> line)
  {
    // Parse account number
    const char * acc = line.c_str();
    input = strtol(acc, &strtolPtr, 10);
    accountNum = input;

    // Parse type of transaction
    r_file >> line;
    if (line == "deposit")
    {
      type = 0;
    }
    else if (line == "withdraw")
    {
      type = 1;
    }
    else
    {
      //error
      type = 0;
    }

    // Parse transaction ammount
    r_file >> line;
    const char * am = line.c_str();
    input = strtol(am, &strtolPtr, 10);  // convert to double!!!!
    ammount = input;

    item slot = {accountNum, type, ammount, pNum};  // Create struct

    int wait;
    int post;

    wait = sem_wait(&E);
    wait = sem_wait(&S);

    boundedBuffer[BufferIn] = slot;
    BufferIn = (BufferIn + 1) % UsableBufferSize;

    post = sem_post(&S);
    post = sem_post(&N);

  }

  sem_wait( &lock );

  ActiveThreads--;

  sem_post( &lock );


  pthread_exit( NULL );

}

void * write_transactions( void * arg )
{

  int wait;
  int post;
  bool workLeft = true;

  /* Continue to consume until all producers are
   finished and buffer is empty */
  while ((ActiveThreads != 0) || (BufferIn != BufferOut) || workLeft)
  {
    workLeft = true;

    wait = sem_wait(&N);
    wait = sem_wait(&S);

    struct item slot = boundedBuffer[BufferOut];
    BufferOut = (BufferOut + 1) % UsableBufferSize;

    post = sem_post(&S);
    post = sem_post(&E);

    ofstream file; // out file stream
    file.open("accounts.new");

    stringstream transaction;
    transaction << slot.prodNum << " ";
    transaction << slot.accNum << " ";
    if (slot.type == 0)
    {
      transaction << "Deposit ";
    }
    else
    {
      transaction << "Withdrawl ";
    }
    transaction << slot.ammount << " ";

    cout << transaction.str() << endl;

    double val;

    for (int n=0; n<accountInfo.size(); n++)
    {
      if (slot.accNum == accountInfo[n].first)
      {
        if (slot.type == 0)
        {
          val = accountInfo[n].second + slot.ammount;
          transaction << accountInfo[n].second << " ";
          transaction << val << endl;
          cout << val << endl;
        }
        else
        {
          val = accountInfo[n].second - slot.ammount;
          transaction << accountInfo[n].second << " ";
          transaction << val << endl;
        }
      }
    }
    file << transaction.str();
    workLeft = false;

  }

}
