import enum
import sys
class Token:
    def __init__(self, tokenText, tokenKind):
        self.text = tokenText   # The token's actual text. Used for identifiers, strings, and numbers.
        self.kind = tokenKind   # The TokenType that this token is classified as.

    def checkIfKeyword(tokenText):
        for kind in TokenType:
            # Relies on all keyword enum values being 1XX.
            if kind.name == tokenText and kind.value >= 100 and kind.value < 200:
                return kind
        return None
class TokenType(enum.Enum):
    PLACEHOLDER = float("inf")
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3
    # Keywords.
    LABEL = 101
    GOTO = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111
    # Operators.
    EQ = 201  
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211
class Lexer:
    def __init__(self, source):
        self.CurPos = -1
        self.CurChar = ""
        self.source = source+"\0"
        self.nextChar()
    def nextChar(self):
        self.CurPos += 1
        if self.CurPos>=len(self.source):self.CurChar="\0"
        else:self.CurChar = self.source[self.CurPos]

    # Return the lookahead character.
    def peek(self):
        if self.CurPos + 1 >= len(self.source):
            return "\0"
        else:
            return self.source[self.CurPos + 1]

    # Invalid token found, print error message and exit.
    def abort(self, message):
        sys.exit("Lexing error. " + message)
		
    # Skip whitespace except newlines, which we will use to indicate the end of a statement.
    def skipWhitespace(self):
        while self.CurChar in " \t\r":
            self.nextChar()
            # print("wite") 
		
    # Skip comments in the code.
    def skipComment(self):
        if self.CurChar == "$":
            self.nextChar()
            while self.CurChar != "$":
                self.nextChar()
            self.nextChar()
    # Return the next token.
    def getToken(self):
        self.skipWhitespace()
        self.skipComment()
        token = None
        
        if self.CurChar == '+':
            token = Token(self.CurChar, TokenType.PLUS)	# Plus token.
        elif self.CurChar == '=':
            if self.peek() == '=':
                lastChar = self.CurChar
                self.nextChar()
                token = Token(lastChar + self.CurChar, TokenType.EQEQ)
            else:
                token = Token(self.CurChar, TokenType.EQ)
        elif self.CurChar == '<':
            if self.peek() == '=':
                self.nextChar()
                token = Token("<=", TokenType.LTEQ)
            else:
                token = Token(self.CurChar, TokenType.LT)
        elif self.CurChar == '>':
            if self.peek() == '=':
                self.nextChar()
                token = Token(">=", TokenType.GTEQ)
            else:
                token = Token(self.CurChar, TokenType.GT)
        elif self.CurChar == '!':
            if self.peek() == '=':
                self.nextChar()
                token = Token("!=", TokenType.NOTEQ)
            else:
                self.abort("Expected != but got !" + self.peek())

        elif self.CurChar == '-':
            token = Token(self.CurChar, TokenType.MINUS)	# Minus token.
        elif self.CurChar == '*':
            token = Token(self.CurChar, TokenType.ASTERISK)	# Asterisk token.
        elif self.CurChar == '/':
            token = Token(self.CurChar, TokenType.SLASH)	# Slash token.
        elif self.CurChar == '\n':
            token = Token(self.CurChar, TokenType.NEWLINE)	# Newline token.
        elif self.CurChar == "\"":  # Beginning of string
            self.nextChar()  # Skip the opening quote
            startPos = self.CurPos
            while self.CurChar != "\"":  # Look for the closing quote
                if self.CurChar == '\0':  # If end of source is reached
                    self.abort("Unterminated string literal.")
                self.nextChar()
            tokText = self.source[startPos : self.CurPos]  # Get the substring
            token = Token(tokText, TokenType.STRING)

        elif self.CurChar in "0123456789":
            startPos = self.CurPos
            while self.peek() in "0123456789":
                self.nextChar()
            if self.peek() == '.': # Decimal
                self.nextChar()
                if not self.peek() in "0123456789": 
                    self.abort("Illegal character in number.")
                while self.peek() in "0123456789":
                    self.nextChar()
            tokText = self.source[startPos : self.curPos + 1] # Get the substring.
            token = Token(tokText, TokenType.NUMBER)
        elif self.CurChar.isalpha():
            startPos = self.CurPos
            while self.peek().isalnum():
                self.nextChar()
            tokText = self.source[startPos : self.CurPos + 1]
            keyword = Token.checkIfKeyword(tokText)
            if keyword == None: # Identifier
                token = Token(tokText, TokenType.IDENT)
            else:   # Keyword
                token = Token(tokText, keyword)
        elif self.CurChar == '\0':
            token = Token(self.CurChar, TokenType.EOF)	# EOF token.
        else:
            self.abort("unknown token: "+"\""+self.CurChar+"\"")
            # pass
        self.nextChar()
        return token #if token else Token("banana",TokenType.PLACEHOLDER)
# source = '+- "abc"== abb <= < >= > *abc'
# lexer = Lexer(source)
# token = lexer.getToken()
# while token.kind != TokenType.EOF:
#     print(token.kind, token.text)
#     token = lexer.getToken()

    