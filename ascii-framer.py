#!/usr/env/python

import sys
import os
from stat import S_ISFIFO

# Global Variables
char = '║'
hchar = '═'
whitespacefiller=' '
maxlinelen=0

stdincontent = []

def argparse():
	"""Parse piped arguments"""
	global char
	# Exit if there is no arguments
	if len(sys.argv) == 1:
		return
	# set the horizonal char with the -c switch
	if len(sys.argv) == 3:
		if sys.argv[1] == '-c':
			char =	sys.argv[2]
	elif len(sys.argv) == 2:
		print('ERROR: not enough arguments given!')
	elif len(sys.argv) > 3:
		print('ERROR: too many arguments given!')
	else:
		print('ARGUMENT ERROR, shit is happening!')
		
def get_stdin():
	"""Populate stdinconent list"""
	# Check if programm is being piped
	if S_ISFIFO(os.fstat(0).st_mode):
		for line in sys.stdin:
			line = line.replace('\n', '')
			line = line.replace('	', '')
			stdincontent.append(line)

def maxlinelencalc():
	# Calculate longest string
	global maxlinelen
	for line in stdincontent:
		if len(line) > maxlinelen:
			maxlinelen = len(line)

def horizontal_line(position):
	# Helper function to draw the top and bottom lines of the frame
	edgechar_l = None
	edgechar_r = None
	if position == 'top':
		edgechar_l = '╔'
		edgechar_r = '╗'
	elif position == 'bottom':
		edgechar_l = '╚'
		edgechar_r = '╝'
	print(f'{edgechar_l}{hchar*(maxlinelen)}{edgechar_r}')	

def framer():
	# Frame string using the horizontal_line helper function
	horizontal_line('top')
	for line in stdincontent:
		print(f'{char}{line}{whitespacefiller*(maxlinelen-len(line))}{char}')
	horizontal_line('bottom')
		
def main():
	argparse()
	get_stdin()
	maxlinelencalc()
	framer()

# Only execute if run as main
if __name__ == "__main__":
	main()
