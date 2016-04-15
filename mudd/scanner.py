from functools import partial
from re import Scanner
from sre_parse import FLAGS
from sys import argv

from mudd import *


def new_line(scanner, token):
    MuddScanner.line_number += 1


def comment_new_line(scanner, token):
    MuddScanner.line_number += token.count('\n')


def scan_error(scanner, token, error_kind):
    raise SyntaxError(error_kind)


def scan_error_partial(error_kind):
    return partial(scan_error, error_kind=error_kind)


def tokenize(scanner, token, token_kind):
    return Token(token_kind, MuddScanner.line_number, token)


def tokenize_partial(token_kind):
    return partial(tokenize, token_kind=token_kind)


token_patterns = [
    (r'/\*.*?\*/', comment_new_line),
    (r'/\*|\*/', scan_error_partial('Comment error')),
    (r'".*?"', tokenize_partial(T_STRLIT)),
    (r'"', scan_error_partial('String literal error.')),
    (r'\n', new_line),
    (r'int(?![a-zA-Z0-9_])', tokenize_partial(T_INT)),
    (r'void(?![a-zA-Z0-9_])', tokenize_partial(T_VOID)),
    (r'string(?![a-zA-Z0-9_])', tokenize_partial(T_STRING)),
    (r'if(?![a-zA-Z0-9_])', tokenize_partial(T_IF)),
    (r'else(?![a-zA-Z0-9_])', tokenize_partial(T_ELSE)),
    (r'while(?![a-zA-Z0-9_])', tokenize_partial(T_WHILE)),
    (r'return(?![a-zA-Z0-9_])', tokenize_partial(T_RETURN)),
    (r'writeln(?![a-zA-Z0-9_])', tokenize_partial(T_WRITELN)),
    (r'write(?![a-zA-Z0-9_])', tokenize_partial(T_WRITE)),
    (r'read(?![a-zA-Z0-9_])', tokenize_partial(T_READ)),
    (r';', tokenize_partial(T_SEMICOL)),
    (r',', tokenize_partial(T_COMMA)),
    (r'\[', tokenize_partial(T_LBRACK)),
    (r'\]', tokenize_partial(T_RBRACK)),
    (r'\{', tokenize_partial(T_LCURLY)),
    (r'\}', tokenize_partial(T_RCURLY)),
    (r'\(', tokenize_partial(T_LPAREN)),
    (r'\)', tokenize_partial(T_RPAREN)),
    (r'<=', tokenize_partial(T_LEQ)),
    (r'<', tokenize_partial(T_LES)),
    (r'==', tokenize_partial(T_EQU)),
    (r'!=', tokenize_partial(T_NEQ)),
    (r'>=', tokenize_partial(T_GEQ)),
    (r'>', tokenize_partial(T_GRE)),
    (r'\+', tokenize_partial(T_PLU)),
    (r'-', tokenize_partial(T_MIN)),
    (r'\*', tokenize_partial(T_MUL)),
    (r'/', tokenize_partial(T_DIV)),
    (r'%', tokenize_partial(T_MOD)),
    (r'&', tokenize_partial(T_AND)),
    (r'=', tokenize_partial(T_ASSIGN)),
    (r'[a-zA-Z][a-zA-Z0-9_]*', tokenize_partial(T_ID)),
    (r'\d+', tokenize_partial(T_NUM)),
    (r'\s+', None),  # ignore whitespace
    (r'.*', scan_error_partial('General error.')),
    ]


class Token():
    def __init__(self, kind, line_number, value=None):
        self.kind = kind
        self.value = value
        self.line_number = line_number
        self.declaration = None

    def __str__(self, level=0):
        return '  '*level+'Token: %s\tValue: %s\t\tLine: %s\n' % (
            str(KIND_NAME[self.kind]), str(self.value), str(self.line_number)
            )


class MuddScanner():
    line_number = 1

    def __init__(self, filename):
        self.filename = filename
        self.data = self._scan_file()
        self.next_token = None
        self.current_index = 0
        self.backtrack_index = []

    def _read_file(self):
        file_string = ''
        with open(self.filename) as f:
            for line in f:
                line = ' '.join(line.split())
                file_string = file_string+'\n'+line
        return file_string[1:]

    def _scan_file(self):
        scanner = Scanner(token_patterns, FLAGS['s'])
        return scanner.scan(self._read_file())[0]

    def get_next_token(self):
        if self.current_index > len(self.data)-1:
            self.next_token = Token(T_EOF, MuddScanner.line_number, None)
        else:
            self.next_token = self.data[self.current_index]
            self.current_index += 1

    def get_line_number(self):
        if self.next_token:
            return self.next_token.line_number
        else:
            return 1

    def backtrack(self):
        self.current_index = self.backtrack_index.pop()
        self.next_token = self.data[self.current_index-1]

    def set_backtrack_index(self):
        self.backtrack_index.append(self.current_index)

    def unset_backtrack_index(self):
        self.backtrack_index.pop()


if __name__ == '__main__':
    try:
        scanner = MuddScanner(argv[1])

        trigger = True
        while trigger:
            scanner.get_next_token()
            token = scanner.next_token
            print(token)
            if token.kind == T_EOF:
                trigger = False

    except IndexError:
        print('[IndexError] No compilable file received as argument.')

    except FileNotFoundError:
        print('[FileNotFoundError] No such file is found.')

    except SyntaxError as e:
        print('[SyntaxError] %s' % e)
