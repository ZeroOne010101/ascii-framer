#!/usr/env/python

import sys
import os
from stat import S_ISFIFO

char = '║'
hchar = '═'
whitespacefiller=' '
maxlinelen=0

stdincontent = []

def argparse():
	global char
	if len(sys.argv) == 1:
		return
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
	#check if programm is being piped
	if S_ISFIFO(os.fstat(0).st_mode):
		for line in sys.stdin:
			line = line.replace('\n', '')
			line = line.replace('	', '    ')
			stdincontent.append(line)

def maxlinelencalc():
	global maxlinelen
	for line in stdincontent:
		if len(line) > maxlinelen:
			maxlinelen = len(line)

def horizontal_line(position):
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
	horizontal_line('top')
	for line in stdincontent:
		print(f'{char}{line}{whitespacefiller*(maxlinelen-len(line))}{char}')
	horizontal_line('bottom')


		
def main():
	argparse()
	get_stdin()
	maxlinelencalc()
	framer()

if __name__ == "__main__":
	main()
