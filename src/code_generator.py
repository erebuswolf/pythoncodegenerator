# code-generator
#Copyright (C) 2007 Jesse Fish
#
#This file is part of code_generator.py
#
#   code_generator.py is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import javacodegen
import Cscodegen
import cppcodegen
import sys

def get_file(i):
	"""determines what file we are reading 

	if there was no file specified at run time, prompts user for file to read"""

	if len(sys.argv)>1:
		infile=sys.argv[i]
	else:
		try:
			infile=raw_input ("no file input given please enter a file name, ctrl-d to quit: ")
		except EOFError:
			print "\nquitting\n"
			exit(0)
	print "reading from file:", infile
	return infile
def read_file(s):
	thefile=get_file(s)
	f=open(thefile,'r')
	#delete useless variables
	del thefile
	text= f.readlines()
	f.close()
	del f
	#remove the newline character
	filetype=(text[0]).strip().lower()
	#get the filename
	filename=(text[1])[:-1]
	print "name of file created:",filename
	if filetype == "java":
		print "type of file being made: JAVA"
		javacodegen.makefile(filename,text)
	elif filetype == "c#":
		print "type of file being made: C#"
		Cscodegen.makefile(filename,text)
	elif filetype == "c++" or filetype == "cpp" :
		print "type of file(s) being made: cpp and h"
		cppcodegen.makefile(filename,text)
	else:
		print "ERROR: unrecognizable file type"
def main():
	"""main function of the program

	basically exists to easily tell where things are called,
	left over idea from C languages"""
	if(len(sys.argv)>1):
		for s in range(1,len(sys.argv)):
			read_file(s)
	else:
		read_file(1)
main()