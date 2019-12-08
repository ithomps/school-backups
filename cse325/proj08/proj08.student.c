/**
 * \file proj08.student.c
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

/// Array of unsigned ints
unsigned int RamStructure[65536][16] {0};

/// Build data cache
struct CacheLine cache[CacheSize];


void displayCache();
void displayLine(string address, string operation, string info);
void readFile(string filename);
string processInstruction(string address, string operation, string data);
int hextoDec(string hex);
void processMiss(string address);
void displayRAM();
string AddSpaces(string input);

/**
 * Builds a data cache that can be modifed by reading a file
 * \param argc Number of command line arguments
 * \param argv[] Array of command line input
 */
 int main(int argc, char *argv[])
 {
   vector<string> files;

   for (int n=0; n<CacheSize; n++)
   {
     /// Init cache to all zeros
     cache[n].V = 0;
     cache[n].M = 0;
     cache[n].tag = "000";
     cache[n].data = "00000000000000000000000000000000";
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
     readFile(files[j]);
   }
   /// After all files have been parsed
   displayCache();

   /// Display Ram at end of program
   displayRAM();

 }  // end main


/**
 * Converts hexadecimal string to int
 * \param hex String in hex
 * \return Integer representation of hex string
 */
int hextoDec(string hex)
{
  return (int)strtol(hex.c_str(), 0, 16);
}

/**
 * Adds spaces in between numbers for formatting
 * \param input String to modify
 * \return Formatted string
 */
string AddSpaces(string input)
{
  string newData;
  for (int i=0; i<input.length(); i+=2)
  {
    newData += input.substr(i, 2);
    newData += " ";
  }
  return newData;

}


/**
 * Displays line fromm file with proper formatting
 * \param address Physical address being referenced
 * \param operation Whether line represents a read or write
 * \param info Hit or Miss followed by data
 */
void displayLine(string address, string operation, string info)
{
  /* Formats and displays memory reference
  Physical address, operation, cache line, tag bits, byte offset
  All seperated by one space
  */

  stringstream output;    // stringstream used to display line

  output << address << " " << operation << " " << address.substr(3,1);
  output << " " << address.substr(0,3) << " " << address.substr(4,1);
  output << " " << info;

  cout << output.str() << endl;
}


/**
 * Function to display contents of cache
 */
void displayCache()
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
    line << AddSpaces(cache[n].data);   // Add data block
    cout << line.str() << endl;

    line.clear();       // clear stringstream
    line.str(string());
  }

  cout << endl;   // terminal blank line

}


/**
 * Displays RAM from address 20000
 * Will display 256 bytes
 */
void displayRAM()
{
  int RamIndex = 20000;
  stringstream line;

  cout << "       0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F" << endl;
  cout << "       -----------------------------------------------" << endl;


  for (int n=RamIndex; n<20016; n++)
  {
    for (int i=0; i<32; i++)
    {
      line << to_string(RamStructure[RamIndex][i]);
    }
    cout << n << ": " << AddSpaces(line.str()) << endl;
    line.clear();
    line.str(string());
  }

}


/**
 * Fucntion to process an instruction from input file
 * \param address Adress in Ram
 * \param opertation Read or Write
 * \param data Data to write with write operation
 * \return Hit or Miss followed by data
 */
string processInstruction(string address, string operation, string data)
{
  string returnString = "";
  string offset = address.substr(4,1);
  int intOffset = hextoDec(offset);

  string index = address.substr(3,1);
  int cacheIndex = hextoDec(index);

  if (!cache[cacheIndex].V)
  {
    processMiss(address);
    returnString += "M ";
  }
  else
  {
    if (address.substr(0,3) != cache[cacheIndex].tag)
    {
      processMiss(address);
      returnString += "M ";
    }
    else
    {
      returnString += "H ";
    }
  } // end if

  cache[cacheIndex].V = true;
  cache[cacheIndex].tag = address.substr(0,3);


  // Miss processing complete
  if (operation == "R")
  {
    returnString += cache[cacheIndex].data.substr(intOffset, 8);
  }
  else if (operation == "W")
  {
    cache[cacheIndex].data.replace(intOffset, 8, data);
    cache[cacheIndex].M = true;
    returnString += cache[cacheIndex].data.substr(intOffset, 8);
  }

  return returnString;

}


/**
 * Brings data up from Ram to cache
 * \param address The address to move up
 */
void processMiss(string address)
{
  // Cache index to replace
  string cacheIndexStr = address.substr(3,1);
  int cacheIndex = hextoDec(cacheIndexStr);

  string tagAddress = address.substr(0,4);
  int ramIndex = hextoDec(tagAddress);

  string offset = address.substr(4,1);
  int ramOffset = hextoDec(offset);

  if (cache[cacheIndex].M == 1)
  {
    string data = cache[cacheIndex].data;
    for (int n=0; n<8; n++)
    {
      RamStructure[ramIndex][ramOffset+n] = int(cache[cacheIndex].data.at(n));
    }
    cache[cacheIndex].M = false;
  }

  // Bring up data from RAM
  string ramData = "";
  for (int i=0; i<32; i++)
  {
    string byte = to_string(RamStructure[ramIndex][i]);
    ramData += byte;
  }

  cache[cacheIndex].data = ramData;

}


/**
 * Function to read file and parse transactions
 * \param filename Name of file to open
 */
void readFile(string filename)
{
  ifstream file;
  file.open(filename);

  if (file.is_open())    // file opened succesfully
  {
    string line;
    string token;
    stringstream ss;
    string data;

    while (!file.eof())
    {

      if (Debug)
      {
        displayCache();   // dump contents of cache
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

            // Extract data for write
            while (ss >> token)
            {
              data += token;
            }

          }
        }

        // Processes instuction from file
        string info = processInstruction(address, operation, data);

        // Formats and prints line
        displayLine(address, operation, info);

        ss.clear();
      }  // end if

    }  // end while
  }  // end if
  else
  {
    cout << "Error opening file" << endl;
  }

}
