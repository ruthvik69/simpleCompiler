import sys
from lxr import *

# Parser object keeps track of current token and checks if the code matches the grammar.
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.curToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken()

    # Return true if the current token matches.
    def checkToken(self, kind):
        return kind==self.curToken.kind

    # Return true if the next token matches.
    def checkPeek(self, kind):
        return kind == self.peekToken.kind

    # Try to match current token. If not, error. Advances the current token.
    def match(self, kind):
        if not self.checkToken(kind):
            self.abort("Expected " + kind.name + ", got " + self.curToken.kind.name)
        self.nextToken()

    # Advances the current token.
    def nextToken(self):
        self.curToken = self.peekToken
        self.peekToken = self.lexer.getToken()

    def abort(self, message):
        sys.exit("Error. " + message)
        
    def program(self):
        print("PROGRAM")

        # Parse all the statements in the program.
        while not self.checkToken(TokenType.EOF):
            self.statement()
    def statement(self):
        if self.checkToken(TokenType.PRINT):
            print("PRINT STATEMENT")
            self.nextToken()
            if self.checkToken(TokenType.STRING):
                self.nextToken()
            else:
                self.expression()
        elif self.checkToken(TokenType.IF):
            print("STATEMENT IF")
            self.nextToken()
            self.comparison()
            self.match(TokenType.THEN)
            self.nl
            while not self.checkToken(TokenType.ENDIF):
                self.statement()
            self.match(TokenType.ENDIF)
        elif self.checkToken(TokenType.WHILE):
            print("STATEMENT WHILE")
            self.nextToken()
            self.comparison()
            self.match(TokenType.REPEAT)
            self.nl()
            while self.checkToken(TokenType.ENDWHILE):
                self.statement()
            self.match(TokenType.ENDWHILE)
            
        elif self.checkToken(TokenType.LABEL):
            print("STATEMENT LABEL")
            self.nextToken()
            self.match(TokenType.IDENT)
        elif self.checkToken(TokenType.GOTO):
            print("STATEMENT GOTO")
            self.nextToken()
            self.match(TokenType.GOTO)
        elif self.checkToken(TokenType.LET):
            print("STATEMENT LET")
            self.nextToken()
            self.match(TokenType.EQ)
            self.match(TokenType.IDENT)
        self.nl()
    def nl(self):
        print("NEWLINE")
        self.match(TokenType.NEWLINE)
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()
    def expression(self):
        pass
a = 'PRINT "abcd"\nPRINT "abcd"\nPRINT "abcd"\nPRINT "abcd"\n'
# if len(sys.argv) != 2:
#     sys.exit("Error: Compiler needs source file as argument.")
# with open(sys.argv[1], 'r') as inputFile:
#     source = inputFile.read()

# Initialize the lexer and parser.
lexer = Lexer(a)
parser = Parser(lexer)

parser.program() # Start the parser.
print("Parsing completed.")
