import sys
import os
import argparse
from stat import S_ISFIFO

# Global Variables
char = '║'
hchar = '═'
whitespacefiller=' '
maxlinelen=0

stdincontent = []

# Setup Argument parser
parser = argparse.ArgumentParser(usage='command | ascii-framer.py [options]', 
		description='This program transforms string input from the commandline to include a nice ascii frame')
parser.add_argument('-c', nargs=1, metavar='value', help='Set a value as the horizonal char')
args = parser.parse_args()

def argparse():
	"""Parse piped arguments"""
	global char, args

	# set the horizonal char with the -c argument
	if args.c:
		char = args.c[0]

		
def get_stdin():
	"""Populate stdinconent list"""
	# Check if programm is being piped
	if S_ISFIFO(os.fstat(0).st_mode):
		for line in sys.stdin:
			line = line.replace('\n', '')
			line = line.replace('	', '')
			stdincontent.append(line)
	else:
		print("Nothing to display")

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
