# File Watcher

Runs a given command when a file is changed.

Example:
	
	# echos the path to a changed .txt file in the ./some/text/files/ directory
	# the -c parameter clears the output whenever the file is changed
	$ watch ./some/text/files/*.txt -c "echo [filepath]"

	# use -o to redirect output
	$ watch ./some/text/files/*.txt -c "echo [filepath]" -o test.txt
	
	# OR (note, this will only dump output when you kill the command)
	$ watch ./some/text/files/*.txt -c "echo [filepath]" >> test.txt
	
Usage:

	File Watcher - written by Corey Walsh
	usage: ./watch.py [options] [file globs] "echo $command-to-run" 
	  -h : display this message
	  -v : verbose
	  -i [int] : milliseconds between file polling
	  -o [filename] : file to dump stdout (appends)
	  -c : clear output before running command

	Standard unix file globs are used for file specification, ex: hello_*.txt

	The following command keywords will be replaced with their corresponding value for the changed file:
	  [filename]
	  [filepath]

Installation:

The easiest way to install this is to simply add a command line alias to your bash profile.
	
	$ export FILE_WATCHER=$(pwd)/watch.py
	$ echo "function watch()  { python $FILE_WATCHER \"\$@\"; }" >> ~/.bashrc

This can be accomplished via the install.sh script

	$ ./install.sh