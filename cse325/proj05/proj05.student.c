/**
 * \file proj04.student.c
 *
 * \author Ian Thompson
 *
 * This program runs a command line interpreter
 */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
#include <pthread.h>
#include <iostream>
#include <string>
#include <sstream>
#include <fstream>

using namespace std;

#define NTHREADS 200

void * thread_function( void * arg );

/// Stores command count
int count = 0;

/**
 * Processes input from the user
 * Executes the command
 * \param input Input from command line
 */
void parse(string user)
{
  bool multiple = false;
  int code;
  int code2;

  string input;
  stringstream ss(user);
  ss >> input;

  if (!ss.eof())
  {
    multiple = true;
  }

  if (input == "halt")
  {
    /// Terminate program
    exit(1);
  }
  else if (input == "help")
  {
    /// Print list of commands
    cout << "halt, help, date, env, path, cwd, cd, set, import" << endl;
  }
  else if (input == "date")
  {
    /// Prints human readable time and date
    time_t unprocessedTime;
    time (&unprocessedTime);
    struct tm *readableTime;
    readableTime = localtime(&unprocessedTime);

    /// Print time
    cout << asctime(readableTime);
  }
  else if (input == "env")
  {
    /// Print list of enviornment variables
    int i = 0;
    while (environ[i] != NULL)
    {
      /// Print each variable and increment
      cout << environ[i] << endl;
      i++;
    }
  }
  else if (input == "path")
  {
    /// Print entire file path
    cout << "PATH: " << getenv("PATH") << endl;
  }
  else if (input == "cwd")
  {
    /// Print current directory
    cout << get_current_dir_name() << endl;
  }
  else if (input == "cd" && multiple == false)
  {
    /// Reset to home directory
    code = chdir("/home");
    code2 = setenv("PWD", get_current_dir_name(), 1);
  }
  else if (input == "cd" && multiple == true)
  {
    /// Change current directory
    /// Load in path argument
    string loc;
    ss >> loc;

    /// Argument used in chdir call
    const char *path;

    if (loc == "~")
    {
      path = "/home";
    }
    else if (loc.at(0) == '~')
    {
      string user = loc.substr(1);
      cout << user << endl;
      user = "/user/" + user;
      path = user.c_str();
    }
    else
    {
      path = loc.c_str();
    }

    code = chdir(path);
    code2 = setenv("PWD", get_current_dir_name(), 1);
  }
  else if (input == "set")
  {
    /// Load in variable
    string var;
    string name;
    ss >> var;

    if (ss.eof())
    {
      code = unsetenv(var.c_str());
    }
    else
    {
      ss >> name;
      code = setenv(var.c_str(), name.c_str(), 1);
    }
  }
  else if (input == "import")
  {
    /// Load in file name
    string filename;
    ss >> filename;
    cout << "File: " << filename << endl;

    ifstream r_file;
    string line;

    r_file.open(filename);
    cout << "Reading file" << endl;

    while (!r_file.eof())
    {
      r_file >> line;
      count++;
      cout << "[" << count << " "<< filename  << "]" << endl;
      parse(line);
    }
  }
  else
  {
    /// Initialize thread variables
    pthread_t mythread;
    int flag;

    flag = pthread_create( &mythread, NULL, &thread_function, &user);

    flag = pthread_join( mythread, NULL );
  }

}

int main()
{
  /// String for parsing input
  string input;

  /// Retrives username from enviornment
  string username = getenv("USER");

  bool running = true;  /// Loops until halt

  while (running)
  {
    string in;  /// Stores user input
    count++;  /// First command is 1

    /// Terminal prompt
    cout << "[" << count << " " << username << "] ";
    getline(cin, input);

    /// Sends token to be parsed and executed
    parse(input);
  }
}

/**
 * Thread function to process external commands
 * \param arg: string from user or file Input
 */
void * thread_function( void * arg )
{
  string input = *static_cast<string*>(arg);
  system(input.c_str());
  pthread_exit( NULL );
}
