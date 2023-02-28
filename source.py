from dataclasses import dataclass
from pathlib import Path

@dataclass
class Line:
	offset: int
	text: str

	def is_preproc(self):
		return self.text.strip().startswith('#')

import cpp

class File:
	def __init__(self, path):
		self.path = Path(path)
		with self.path.open() as fp:
			self.lines = [Line(*tupl) for tupl in enumerate(fp)]

	def __iter__(self):
		for line in self.lines:
			if line.is_preproc() and (obj := cpp.parse(line)):
				yield (line, obj)
			else:
				yield (line, None)

