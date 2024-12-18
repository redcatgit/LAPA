from antlr4 import Parser

class CPP14ParserBase(Parser):
    """
    Base parser class for CPP14Parser.
    All parsing methods required by CPP14Parser should be implemented here.
    """
    def __init__(self, input, output=None):
        super().__init__(input)
        self.output = output
