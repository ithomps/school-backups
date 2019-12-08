/**
 * \file proj09.student.c
 *
 * \author Ian Thompson
 *
 * A program to simulate managing primary storage using paging
 */

#include <iostream>
#include <iomanip>
#include <vector>
#include <string>
#include <fstream>

using namespace std;

/// Declared functions
void readFile(string filename);
unsigned int pageNum(unsigned int address);
unsigned int byteOffset(unsigned int address);
void dumpPageTable();
void processInstruction(string address, string operation);
void displaySummaryInfo();


/// Struct to represent a line of the page table
struct pageLine
{
	bool valid = 0;				// If page is present in table
	bool referenced = 0;		// If page has been referenced recently
	bool modified = 0;			// If page has been modified
	unsigned int frameNumber = 0x0000;		// Logical address assosiated with this page
};

/// Number of entries in the page table
const int PageTableSize = 8;

/// If project is in debug mode
bool Debug = 0;

/// Summary information
int MemoryReferences = 0;
int ReadInstructions = 0;
int WriteInstructions = 0;

/// Create the page table initialized to all zeros
pageLine PageTable[PageTableSize];


/**
 * Simulates a paging system using a page table
 * that is represented by an array of structs
 *
 * \param argc The number of command line arguments
 * \param argv Array of command line arguments
 */
int main(int argc, char *argv[])
{
  /// Holds files containing memory references
  vector<string> files;

  /// Process all command line arguments
  for (int i=1; i<argc; i++)
  {

    if (string(argv[i]) == "-debug")
    {
      /// Display page table on each memory reference
      Debug = 1;
    }
    else if (string(argv[i]) == "-refs")
    {
      /// Next argument will be a filename
      files.push_back(string(argv[i+1]));
      i++;
    }
    else
    {
      cout << "Unknown token: " << argv[i] << endl;
    }

  }  // end for

  /// Process all input files
  for (size_t j=0; j<files.size(); j++)
  {
    readFile(files[j]);
  }

  /// Display data after files have processed
  dumpPageTable();

  /// Display memory reference data
  displaySummaryInfo();

} // end main


/**
 * Displays summary of memory references
 */
void displaySummaryInfo()
{
  /// Format and display instuction information
  cout << "Total Memory References: " << MemoryReferences << endl;
  cout << "Total Read Operations: " << ReadInstructions << endl;
  cout << "Total Write Operations: " << WriteInstructions << endl;
}


/**
 * Processes a line from the input file
 * and output information about instuction
 *
 * \param address Logical address referenced
 * \param operation Read or write to preform
 */
void processInstruction(string address, string operation)
{
  /// Convert address from a string to an unsigned int
  unsigned int logicalAddress = stoul(address, nullptr, 16);

  /// Adjust summary values
  MemoryReferences++;

  if (operation == "R")
  {
    ReadInstructions++;
  }
  else if (operation == "W")
  {
    WriteInstructions++;
  }
  else
  {
    cout << "Invalid instuction: " << operation << endl;
    exit(-1);
  }

  /// Output details of instuction
  cout << hex << setfill('0') << setw(4) << logicalAddress << " ";
  cout << operation << " ";
  cout << hex << pageNum(logicalAddress) << " ";
  cout << hex << setfill('0') << setw(3) << byteOffset(logicalAddress) << endl;

} // end processInstruction


/**
 * Opens and reads a file of memory references
 * \param filename The name of the file to read
 */
void readFile(string filename)
{
  /// Strings for processing file
  stringstream ss;
  string line;
  string address;
  string operation;

  /// Open and parse file
  ifstream file;
  file.open(filename);

  if (file.is_open())   // If file opened succesfully
  {

    while (!file.eof())
    {
      /// Bring line into stringstream
      getline(file, line);
      ss << line;

      if (line != "")     // Ignore empty lines
      {

        if (Debug)
        {
          dumpPageTable();    // Display page table
        } // end if


        /// Parse information from line
        ss >> address;
        ss >> operation;

        /// Process instruction from line
        processInstruction(address, operation);

      } // end if

      ss.clear();     // Reset stringstream

    } // end while

  } // end if

} // end readFile


/**
 * Uses masking and shifting to extract
 * the page number from an address
 *
 * \param address Logical address

 * \return The page number contained in the address
 */
unsigned int pageNum(unsigned int address)
{
	return (address & 0x3800) >> 11;
}


/**
 * Uses masking to extract the byte offset
 *
 * \param address Logical address
 *
 * \return The byte offset contained in the address
 */
unsigned int byteOffset(unsigned int address)
{
	return address & 0x7FF;
}


/**
 * Formats and displays the contents of the page table
 */
void dumpPageTable()
{
	/// Display headers
  cout << endl;
	cout << "     V R M Frame" << endl;
	cout << "     ----- ------" << endl;

	/// Dump Contents
	for (int i = 0; i < PageTableSize; i++)
	{
		cout << "[" << i << "]: ";					// Display index
		cout << PageTable[i].valid << " ";			// Display valid bit
		cout << PageTable[i].referenced << " ";		// Display referenced bit
		cout << PageTable[i].modified << " ";		// Display modified bit

		/// Display frame number in hexadecimal with leading zeros
		cout << "0x";
		cout << hex << setfill('0') << setw(4) << PageTable[i].frameNumber << endl;

	} // end for

  cout << endl;

} // end dumpPageTable
