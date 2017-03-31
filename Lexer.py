from Constants import *


class Token(object):
    """Token type."""

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return "Token(%s, %r)" % (self.type, self.value)

    __repr__ = __str__


class Lexer(object):
    """
        Lexer. Lexical analyzer.
        Interface: get_next_token(): Lexical analyze the next token;
                   get_local_text(): Get the lexical-analyzing local texts.
    """

    def __init__(self, text):
        self.text = text
        self.pos = 1
        self.current_char = text[0]

    def Error(self, errstr):
        raise SyntaxError(errstr)

    def advance(self):
        if self.pos == len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
            self.pos += 1

    def peek(self):
        if self.pos >= len(self.text) - 1:
            return None
        else:
            return self.text[self.pos]

    def get_local_text(self, length=5):
        ans = ''
        if self.pos - 1 - length > 0:
            ans += '...'
        ans += self.text[max(self.pos - 1 - length, 0): min(self.pos - 1 + length, len(self.text))]
        if self.pos - 1 + length < len(self.text):
            ans += '...'
        return ans

    def skip_space(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_NAME(self):
        ans = ''
        while self.current_char is not None and (self.current_char.isalpha() or
                                                 self.current_char == '_' or
                                                 self.current_char.isdigit()):
            ans += self.current_char
            self.advance()
        if ans in RESERVED:
            return Token(RESERVED[ans], ans)
        else:
            return Token(NAME, ans)

    def get_number(self):
        ans = ''
        while self.current_char is not None and self.current_char.isdigit():
            ans += self.current_char
            self.advance()
        if self.current_char == '.':
            ok = False
            ans += self.current_char
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                ans += self.current_char
                self.advance()
                ok = True
            if not ok:
                self.Error('Lexical analyze error at "%s"' % self.get_local_text())
        if self.current_char == 'e':
            ans += 'e'
            self.advance()
            if self.current_char == '-':
                ans += '-'
                self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                ans += self.current_char
                self.advance()
        return Token(NUM, float(ans))

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_space()
                continue
            elif self.current_char.isdigit() or self.current_char == '.':
                return self.get_number()
            elif self.peek() is not None and self.current_char + self.peek() in TwoCharSymbols:
                c = self.current_char + self.peek()
                self.advance()
                self.advance()
                return Token(TwoCharSymbols[c], c)
            elif self.current_char in OneCharSymbols:
                c = self.current_char
                self.advance()
                return Token(OneCharSymbols[c], c)
            elif self.current_char.isalpha() or self.current_char == '_':
                return self.get_NAME()
            else:
                self.Error('parse error at "%s"' % self.get_local_text())
        return Token(EOF, None)
