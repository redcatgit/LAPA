from antlr4 import Lexer

class Java9LexerBase(Lexer):
    """
    Base lexer class for Java9Lexer.
    All lexer methods required by Java9Lexer should be implemented here.
    """
    def __init__(self, input, output=None):
        super().__init__(input)
        self.output = output
