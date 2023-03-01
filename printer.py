import source
import sys
import cpp
from dataclasses import dataclass

class FilePrinter:
	@dataclass
	class Block:
		parent: object
		depth: int
		evaled_true: bool
		enabled: bool

		def try_enable(self):
			self.enabled = self.parent.enabled if self.parent else True
			if self.enabled:
				self.evaled_true = True

		def next(self, evaled):
			return FilePrinter.Block(self, self.depth + 1, evaled, evaled and self.enabled)

	def __init__(self, file, outfp, defines={}):
		self.file = file
		self.defines = defines
		self.outfp = outfp

		# Current conditional block
		self.block = FilePrinter.Block(None, 0, True, True)
		
		# We do this to preserve tabs since they might get expanded and mess up the offset
		from string import printable, whitespace
		nonws = map(ord, set(printable) - set(whitespace))
		self.empty_tr = dict.fromkeys(nonws, ' ')

	def eval_expr(self, expr):
		# TODO: actually eval the expression, for now just mock return values
		if 'ZEND_MM_CUSTOM' in expr:
			return True
		return False

	def print_line(self, line, hide=False):
		if not self.block.enabled or hide:
			print(line.text.translate(self.empty_tr), end='', file=self.outfp)
		else:
			print(line.text, end='', file=self.outfp)

	def push_block(self, evaled):
		self.block = self.block.next(evaled)

	def pop_block(self):
		self.block = self.block.parent
	
	def print(self):
		for (line, obj) in self.file:
			match obj:
				case cpp.If(expr=expr)|cpp.Ifdef(expr=expr)|cpp.Ifndef(expr=expr):
					result = self.eval_expr(expr)
					self.push_block(result)
				case cpp.Elif(expr=expr):
					if self.block.evaled_true:
						self.block.enabled = False
					elif self.eval_expr(expr):
						self.block.try_enable()
				case cpp.Else():
					if self.block.evaled_true:
						self.block.enabled = False
					else:
						self.block.try_enable()
				case cpp.Endif():
					self.pop_block()
			self.print_line(line, hide=(obj != None))

