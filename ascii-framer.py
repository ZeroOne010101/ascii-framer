#!/usr/env/python

import sys
import os
from stat import S_ISFIFO


def get_content_as_list():
	"""Returns the content as a list of lines"""
	if not check_if_piped():
		content_lines = sys.argv[1].split("\n")
	else:
		content_lines = sys.stdin
	
	return content_lines


def check_if_piped():
	"""Check if the program has had input piped into it"""
	return S_ISFIFO(os.fstat(0).st_mode)


def argparse():
	"""Parse arguments whether content was given as one or piped in"""
	char = '║'
	unpiped_offset = 0 if check_if_piped() else 1
	# Exit if there is no arguments
	if len(sys.argv) == 1:
		return char
	# set the horizontal char with the -c switch
	if len(sys.argv) == 3 + unpiped_offset:
		if sys.argv[1 + unpiped_offset] == '-c':
			char =	sys.argv[2 + unpiped_offset]
	elif len(sys.argv) == 2 + unpiped_offset:
		print('ERROR: not enough arguments given!')
	elif len(sys.argv) > 3 + unpiped_offset:
		print('ERROR: too many arguments given!')
		
	return char

		
def clean_content_list(content_lines):
	"""Format the content ready for display within the frame"""
	cleaned_content_list = []
	for line in content_lines:
		line = line.replace('\n', '')
		line = line.replace('	', '')
		cleaned_content_list.append(line)
		
	return cleaned_content_list


def max_line_calc(content_lines):
	"""Calculate the longest line in content_lines"""
	max_line_length = 0
	for line in content_lines:
		if len(line) > max_line_length:
			max_line_length = len(line)
	
	return max_line_length
			

def horizontal_line(position, max_line_length):
	"""Helper function to draw the top and bottom lines of the frame"""
	edgechar_l = None
	edgechar_r = None
	if position == 'top':
		edgechar_l = '╔'
		edgechar_r = '╗'
	elif position == 'bottom':
		edgechar_l = '╚'
		edgechar_r = '╝'
	print(f'{edgechar_l}{"="*(max_line_length)}{edgechar_r}')	


def framer(content_lines, max_line_length, char):
	"""Frame string using the horizontal_line helper function"""
	horizontal_line('top', max_line_length)
	for line in content_lines:
		print(f'{char}{line}{" "*(max_line_length-len(line))}{char}')
	horizontal_line('bottom', max_line_length)
		
def main():
	content_lines = get_content_as_list()
	char = argparse()
	content_lines = clean_content_list(content_lines)
	max_line_length = max_line_calc(content_lines)
	framer(content_lines, max_line_length, char)

# Only execute if run as main
if __name__ == "__main__":
	main()
