/**
 * \file proj10.student.c
 *
 * \author Ian Thompson
 *
 * A program to simulate managing primary storage using paging
 *
 * Extends Project 09, adding a way to edit the page table
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
void readConfig();
bool processFault(unsigned int pageNumber);
bool replaceCLOCK();
bool replaceFIFO();


/// Struct to represent a line of the page table
struct pageLine
{
	bool valid = 0;					// If page is present in table
	bool referenced = 0;		// If page has been referenced recently
	bool modified = 0;			// If page has been modified
	unsigned int frameNumber = 0x0000;		// Logical address assosiated with this page
};

/// Vector to represent the free frame list
vector<unsigned int> FreeFrameList;

/// Vector containing page numbers to allow for FIFO
vector<int> PagesAllocatedInOrder;

/// Number of entries in the page table
const int PageTableSize = 8;

/// If project is in debug mode
bool Debug = 0;

/// Page replacement algorithm
/// Clock = 0 : FIFO = 1
bool PageReplacementAlg = 0;

/// Summary information
int MemoryReferences = 0;
int ReadInstructions = 0;
int WriteInstructions = 0;
int PageFaultCount = 0;
int WriteBackCount = 0;
int NumberOfAllocatedFrames;
string FrameNumberString;

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
	// Read the config file to allocate memory
	readConfig();

  // Holds files containing memory references
  vector<string> files;

  // Process all command line arguments
  for (int i=1; i<argc; i++)
  {

    if (string(argv[i]) == "-debug")
    {
      // Display page table on each memory reference
      Debug = 1;
    }
    else if (string(argv[i]) == "-refs")
    {
      // Next argument will be a filename
      files.push_back(string(argv[i+1]));
      i++;
    }
    else
    {
      cout << "Unknown token: " << argv[i] << endl;
    }

  }  // end for

  // Process all input files
  for (size_t j=0; j<files.size(); j++)
  {
    readFile(files[j]);
  }

  // Display data after files have processed
  dumpPageTable();

  // Display memory reference data
  displaySummaryInfo();

} // end main


/**
 * Displays summary of memory references
 */
void displaySummaryInfo()
{
	// Determine replacment algorithm
	string alg;
	if (PageReplacementAlg)
	{
		alg = "FIFO ";
	}
	else
	{
		alg = "CLOCK ";
	}

  // Format and display instuction information
	cout << alg << "Algorithm Simulation With ";
	cout << NumberOfAllocatedFrames << " Page Frames" << endl;
  cout << "Total Memory References: " << MemoryReferences << endl;
  cout << "Total Read Operations: " << ReadInstructions << endl;
  cout << "Total Write Operations: " << WriteInstructions << endl;
	cout << "Total Page Faults: " << PageFaultCount << endl;
	cout << "Total Write Backs: " << WriteBackCount << endl;
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
  // Split address into components
  unsigned int logicalAddress = stoul(address, nullptr, 16);
	unsigned int pageNumber = pageNum(logicalAddress);
	unsigned int pageByteOffset = byteOffset(logicalAddress);

	// Track page faults and write backs to display with instruction
	bool pageFaultOccured = false;
	bool writeBackFaultOccurred = false;

  // Adjust summary values
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

	// Check if entry is invalid
	if (PageTable[pageNumber].valid == 0)
	{
		// Process page fault
		bool wb = processFault(pageNumber);
		if (wb)
		{
			WriteBackCount++;
			writeBackFaultOccurred = true;
		}
		PageFaultCount++;
		pageFaultOccured = true;
	}

	// Process instuction
	PageTable[pageNumber].referenced = 1;

	if (operation == "W")
	{
		PageTable[pageNumber].modified = 1;
	}

	// Format instuction information
	char pf = ' ';
	char wb = ' ';
	if (pageFaultOccured)
	{
		pf = 'F';
	}
	if (writeBackFaultOccurred)
	{
		wb = 'B';
	}

	// Calculate physical address
	unsigned int physicalAddress = PageTable[pageNumber].frameNumber;
	physicalAddress = physicalAddress << 11 | pageByteOffset;

  // Output details of instuction
  cout << hex << setfill('0') << setw(4) << logicalAddress << " ";
  cout << operation << " ";
  cout << hex << pageNumber << " ";
  cout << hex << setfill('0') << setw(3) << pageByteOffset << " ";
	cout << pf << " " << wb << " ";
	cout << hex << setfill('0') << setw(6) << physicalAddress << endl;

} // end processInstruction


/**
 * Bring a page into RAM using the
 * free frame list and specified replacement algorithm
 *
 * \param pageNumber Page table entry to make valid
 * \return If a write back fault occurred
 */
bool processFault(unsigned int pageNumber)
{
	// Check if there is a frame avalible
	if (!FreeFrameList.empty())
	{
		// Bring page up from disk and update its entry
		PageTable[pageNumber].valid = 1;
		PageTable[pageNumber].referenced = 0;
		PageTable[pageNumber].modified = 0;

		// Use first avalible frame
		PageTable[pageNumber].frameNumber = FreeFrameList.at(0);
		FreeFrameList.erase(FreeFrameList.begin());

		// Adjust FIFO data structure
		if (PageReplacementAlg)
		{
			// FIFO circular buffer
			PagesAllocatedInOrder.push_back(pageNumber);
		}

	}
	else
	{
		// Select and free a victim frame
		if (PageReplacementAlg)
		{
			// Preform page replacment using FIFO algorithm
			bool wb = replaceFIFO();

			// Preform page fault processing with a free frame
			processFault(pageNumber);

			// Return true if there was a write back fault
			return wb;
		}
		else
		{
			// Preform page replacement using clock algorithm
			bool wb = replaceCLOCK();

			// Preform page fault processing with a free frame
			processFault(pageNumber);

			// Return true if there was a write back fault
			return wb;
		}
	}

	return false;

} // end processFault


/**
 * Free a page frame using the FIFO algorithm
 * \return If there was a write back
 */
bool replaceFIFO()
{
	// Track if a write back fault occurs
	bool writeBack = false;

	// Get index of entry to replace and advance buffer
	int pageNumber = PagesAllocatedInOrder.at(0);
	PagesAllocatedInOrder.erase(PagesAllocatedInOrder.begin());

	// Determine if entry has been edited
	if (PageTable[pageNumber].modified == 1)
	{
		writeBack = true;		// Entry was modified and must be stored back to disk
	}

	// Extract frame number from entry
	FreeFrameList.push_back(PageTable[pageNumber].frameNumber);

	// Invalidate entry
	PageTable[pageNumber].valid = 0;

	return writeBack;

} // end replaceFIFO


/**
 * Free a page using the clock algorithm
 * \return If there was a write back
 */
bool replaceCLOCK()
{
	// Track if a write back fault occurs
	bool writeBack = false;

	// Only remove one entry
	bool evictedEntry = false;

	// Iterate over entire page table
	for (int n=0; n<PageTableSize; n++)
	{
		// If entry is valid and not used recently
		if (PageTable[n].valid == 1 && PageTable[n].referenced == 0 && !evictedEntry)
		{
			// Check for write back fault
			if (PageTable[n].modified == 1)
			{
				writeBack = true;
			}

			// Remove entry and free frame number
			FreeFrameList.push_back(PageTable[n].frameNumber);
			PageTable[n].valid = 0;
			evictedEntry = true;
		}

		// Reset referenced bit in all entries
		PageTable[n].referenced = 0;

	} // end for

	// If no candidate was found, default to FIFO
	if (!evictedEntry)
	{
		return replaceCLOCK();
	}

	return writeBack;

} // end replaceCLOCK


/**
 * Opens and reads a file of memory references
 * \param filename The name of the file to read
 */
void readFile(string filename)
{
  // Strings for processing file
  stringstream ss;
  string line;
  string address;
  string operation;

  // Open and parse file
  ifstream file;
  file.open(filename);

  if (file.is_open())   // If file opened succesfully
  {

    while (!file.eof())
    {
      // Bring line into stringstream
      getline(file, line);
      ss << line;

      if (line != "")     // Ignore empty lines
      {

        if (Debug)
        {
          dumpPageTable();    // Display page table
        } // end if


        // Parse information from line
        ss >> address;
        ss >> operation;

        // Process instruction from line
        processInstruction(address, operation);

      } // end if

      ss.clear();     // Reset stringstream

    } // end while

  } // end if

} // end readFile


/**
 * Read in the config file located in this directory
 */
void readConfig()
{
	// Variables to process config file
	string filename = "config";
  stringstream ss;
  string line;
	int framesAllocated;
	unsigned int address;

	// Open and parse file
  ifstream file;
  file.open(filename);

	if (file.is_open())   // If file opened succesfully
	{
		// Algorithm for page replacement
		getline(file, line);

		if (line == "CLOCK")
		{
			PageReplacementAlg = 0;		// Select clock algorithm
		}
		else
		{
			PageReplacementAlg = 1;		// Select first in first out algorithm
		}

		// Page frames allocated to this process
		getline(file, line);
		framesAllocated = stol(line,nullptr,10);
		NumberOfAllocatedFrames = framesAllocated;

		// Physical addresses of the free frame list
		getline(file, line);

		// Save to display with summary info
		FrameNumberString = line;

		// Parse addresses with a stringstream
		ss << line;
		line = "";

		// Convert address from a string to an unsigned int, base 16
		for (int n=0; n<framesAllocated; n++)
		{
			ss >> line;
		  address = stoul(line, nullptr, 16);

			FreeFrameList.push_back(address);

		}
	}

} // end readConfig


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
	// Display headers
  cout << endl;
	cout << "     V R M Frame" << endl;
	cout << "     ----- ------" << endl;

	// Dump Contents
	for (int i = 0; i < PageTableSize; i++)
	{
		cout << "[" << i << "]: ";					// Display index
		cout << PageTable[i].valid << " ";			// Display valid bit
		cout << PageTable[i].referenced << " ";		// Display referenced bit
		cout << PageTable[i].modified << " ";		// Display modified bit

		// Display frame number in hexadecimal with leading zeros
		cout << "0x";
		cout << hex << setfill('0') << setw(4) << PageTable[i].frameNumber << endl;

	} // end for

  cout << endl;

} // end dumpPageTable
