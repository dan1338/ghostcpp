from dataclasses import dataclass
import re
import source

def cppre(s):
	def decorator(cls):
		cls.match = re.compile(s).match
		return cls
	return decorator

@cppre('\s*#\s*if\s+(.+)')
@dataclass
class If:
	line: source.Line
	expr: str

@cppre('\s*#\s*ifdef\s+(.+)')
@dataclass
class Ifdef:
	line: source.Line
	expr: str

@cppre('\s*#\s*ifndef\s+(.+)')
@dataclass
class Ifndef:
	line: source.Line
	expr: str

@cppre('\s*#\s*elif\s+(.+)')
@dataclass
class Elif:
	line: source.Line
	expr: str

@cppre('\s*#\s*else')
@dataclass
class Else:
	line: source.Line

@cppre('\s*#\s*endif')
@dataclass
class Endif:
	line: source.Line

cpp_types = [If, Ifdef, Ifndef, Elif, Else, Endif]
try_make = lambda cls, line: cls(line, *m.groups()) if (m := cls.match(line.text)) else None

is_cond = lambda x: 'expr' in dir(x)

def parse(line):
	for cls in cpp_types:
		if ret := try_make(cls, line):
			return ret
	return None

