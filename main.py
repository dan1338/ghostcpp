import sys
import source
from printer import FilePrinter
from getopt import gnu_getopt

def usage():
	print('usage: %s [-D key=val]... [-o out] file' % sys.argv[0])
	sys.exit(1)

defines = dict()
outpath = None

opts, args = gnu_getopt(sys.argv[1:], 'o:D:')

if len(args) != 1:
	usage()

for (opt, arg) in opts:
	if opt == '-D' and arg:
		match arg.split('='):
			case (key, val): defines[key] = val
			case (key,): defines[key] = None
	elif opt == '-o' and arg:
		outpath = arg

outfile = open(outpath, 'w') if outpath else sys.stdout

f = source.File(args[0])
FilePrinter(f, outfile, defines=defines).print()

