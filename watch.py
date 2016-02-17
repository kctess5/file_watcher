#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import sys
import time
import glob2
import subprocess

class File():
	def __init__(self, name):
		self.last_updated = os.stat(name).st_mtime
		self.name = name
		self.fullname = os.path.abspath(name)

	def lastModified(self):
		return os.stat(self.name).st_mtime

	def update(self):
		self.last_updated = self.lastModified()

	def dirty(self):
		return self.lastModified() != self.last_updated

	def exists(self):
		return os.path.isfile(self.fullname)

class ProgramOptions(object):
	"""Holds the program options, after they are parsed by parse_options()"""

	def __init__(self, args):
		self.poll_interval = 500 #ms
		self.command = ""
		self.files = []
		self.output = "console"
		self.verbose = False
		self.clear = False
		self.bash_file = ''

		self.parse(args)

	def parse(self, args):
		parsed_args = {}
		skip = set()

		if len(args) < 2:
			print "Not enough arguments.\n"
			self.printUsage()
			exit(1)
		
		for i in xrange(len(args)):
			if args[i][0] == '-':
				val = ' '
				skip.add(i)

				if args[i] not in ['-h', '-v', '-c']:
					skip.add(i+1)
					val = args[i+1]

				parsed_args[args[i]] = val

		other_args = filter(lambda x:  not x in skip, xrange(len(args)))
		args = map(lambda x: args[x], other_args)

		if '-h' in parsed_args:
			self.printUsage()

		if '-i' in parsed_args:
			self.poll_interval = float(parsed_args['-i'])

		if '-v' in parsed_args:
			self.verbose = True

		if '-c' in parsed_args:
			self.clear = True

		if '-o' in parsed_args:
			self.output = parsed_args['-o']

		if '-env' in parsed_args:
			self.bash_file = parsed_args['-env']

		self.parseGlobs(args[:-1] )
		self.command = args[-1]

	def parseGlobs(self, file_globs):
		for file_glob in file_globs:
			for file_name in glob2.glob(file_glob):
				self.files.append(File(file_name))

	def printUsage(self):
		print "File Watcher - written by Corey Walsh"
		print "usage: ./watch.py [options] [file globs] \"echo $command-to-run\" "
		print "  -h : display this message"
		print "  -v : verbose"
		print "  -i [int] : milliseconds between file polling"
		print "  -o [filename] : file to dump stdout (appends)"
		print "  -c : clear output before running command"
		print
		print "Standard unix file globs are used for file specification, ex: hello_*.txt"
		print
		print "The following command keywords will be replaced with their corresponding value for the changed file:"
		print "  [filename]"
		print "  [filepath]"

def main():
	options = ProgramOptions(sys.argv[1:])

	if options.verbose:
		print "Watching files:"
		for i in options.files:
			print "  ", i.name
		print "Polling every:", options.poll_interval, "ms"
		print "Outputting to:", options.output
	else:
		print "Watching", len(options.files), \
			  "files every", options.poll_interval, \
			  "ms. Outputting stdout to", options.output

	if options.output == 'console':
		_outFile = subprocess.PIPE
	else:
		_outFile = open(options.output, "a")

	def run(cmd):
		if options.verbose:
			print "Running Command:", cmd

		if options.clear:
			subprocess.call('clear',shell=True)

		if options.output == 'console':
			print subprocess.Popen(command, shell=True, stdout=_outFile).stdout.read()
		else:
			subprocess.Popen(command, shell=True, stdout=_outFile)

	# poll all files after sleeping for the desired interval
	while True:
		time.sleep(options.poll_interval / 1000.0)

		# handle the case where the file is deleted
		options.files = [f for f in options.files if f.exists()]
		
		for f in options.files:
			# if the file has been modified since it was last updated
			if f.dirty():
				f.update()
				command = options.command.replace("[filename]", f.name)
				command = command.replace("[filepath]", f.fullname)
				run(command)

if __name__ == "__main__":
	main()
