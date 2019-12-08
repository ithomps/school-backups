/**
 * \file proj07.student.c
 *
 * \author Ian Thompson
 *
 * Program to implement a direct mapped cache
 */

#include <iostream>
#include <iomanip>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>

#define CacheSize 16    // Size of cache
bool Debug = 0;         // If project is in debug mode

using namespace std;

/// Struct to represent 1 line of cache
struct CacheLine
{
  bool V;       // Valid bit
  bool M;       // Modified bit
  string tag;   // Tag of address
  string data;  // 16 bytes of data
};

void displayCache(struct CacheLine cache[]);
void displayLine(string address, string operation);
void readFile(string filename, struct CacheLine cache[]);

/**
 * Builds a data cache that can be modifed by reading a file
 * \param argc Number of command line arguments
 * \param argv[] Array of command line input
 */
 int main(int argc, char *argv[])
 {
   /// Build data cache
   struct CacheLine cache[CacheSize];

   vector<string> files;

   for (int n=0; n<CacheSize; n++)
   {
     /// Init cache to all zeros
     cache[n].V = 0;
     cache[n].M = 0;
     cache[n].tag = "000";
     cache[n].data = "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00";
   }

   for (int i=1; i<argc; i++)   // process all command line arguments
   {

     if (string(argv[i]) == "-debug")
     {
       // Display cache upon each entry from file
       Debug = 1;
     }
     else if (string(argv[i]) == "-refs")
     {
       // Next argument will be a filename
       files.push_back(string(argv[i+1]));
     }  // end else if

   }  // end for

   for (size_t j=0; j<files.size(); j++)
   {
     readFile(files[j], cache);
   }
   /// After all files have been parsed
   displayCache(cache);

 }  // end main


/**
 * Displays line fromm file with proper formatting
 * \param address Physical address being referenced
 * \param operation Whether line represents a read or write
 */
 void displayLine(string address, string operation)
 {
   /* Formats and displays memory reference
    Physical address, operation, cache line, tag bits, byte offset
    All seperated by one space
    */

   stringstream output;    // stringstream used to display line

   output << address << " " << operation << " " << address.substr(3,1);
   output << " " << address.substr(0,3) << " " << address.substr(4,1);

   cout << output.str() << endl;
 }

/**
 * Function to display contents of cache
 * \param cache Array of type struct containing cache
 */
void displayCache(struct CacheLine cache[])
{
  /// Stringstream to hold cache line
  stringstream line;

  /// Display header
  cout << endl;
  cout << "     V M Tag Block" << endl;
  cout << "     ------- -----------------------------------------------" << endl;

  for (int n=0; n<CacheSize; n++)
  {
    line << "[" << hex << n << "]: ";
    line << cache[n].V << " ";          // Add valid bit
    line << cache[n].M << " ";          // Add modifed bit
    line << cache[n].tag << " ";        // Add tag
    line << cache[n].data;              // Add data block
    cout << line.str() << endl;

    line.clear();       // clear stringstream
    line.str(string());
  }

  cout << endl;   // terminal blank line

}

/**
 * Function to read file and parse transactions
 * \param filename Name of file to open
 * \param cache Array of type struct containing cache
 */
void readFile(string filename, struct CacheLine cache[])
{
  ifstream file;
  file.open(filename);

  if (file.is_open())    // file opened succesfully
  {
    string line;
    string token;
    stringstream ss;

    while (!file.eof())
    {

      if (Debug)
      {
        displayCache(cache);   // dump contents of cache
      }

      string address;
      string operation;

      getline(file, line);
      ss << line;

      if (line != "")
      {
        while (ss >> token)
        {
          if (token.length() == 5)    // Physical address
          {
            address = token;
          }
          else if (token == "R")      // Read operation
          {
            operation = token;
          }
          else if (token == "W")      // Write operation
          {
            operation = token;
          }
        }

        displayLine(address, operation);   // formats and prints line

        ss.clear();
      }  // end if

    }  // end while
  }  // end if
  else
  {
    cout << "Error opening file" << endl;
  }

}
