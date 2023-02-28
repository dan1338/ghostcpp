import sys
import source
from printer import FilePrinter

# TODO: Add cli level compatibility with cpp

if __name__ == '__main__':
	files = list(map(source.File, sys.argv[1:]))

	for file in files:
		FilePrinter(file, sys.stdout).print()

