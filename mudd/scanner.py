from re import Scanner
from sre_parse import FLAGS
from sys import argv

from mudd import *


class Token():
    def __init__(self, kind, line_number, value=None):
        self.kind = kind
        self.value = value
        self.line_number = line_number

    def __repr__(self):
        return 'Kind: %s\tValue: %s\t\tLine: %s' % (
            str(self.kind), str(self.value), str(self.line_number)
            )


class MuddScanner():
    line_number = 1

    def __init__(self, filename):
        self.filename = filename
        self.data = self._scan_file()
        self.next_token = None
        self.current_index = 0
        # self.current_line = 1

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


def t_int(scanner, token):
    return Token(T_INT, MuddScanner.line_number, token)


def t_num(scanner, token):
    return Token(T_NUM, MuddScanner.line_number, token)


def t_id(scanner, token):
    return Token(T_ID, MuddScanner.line_number, token)


def t_void(scanner, token):
    return Token(T_VOID, MuddScanner.line_number, token)


def t_string(scanner, token):
    return Token(T_STRING, MuddScanner.line_number, token)


def t_if(scanner, token):
    return Token(T_IF, MuddScanner.line_number, token)


def t_else(scanner, token):
    return Token(T_ELSE, MuddScanner.line_number, token)


def t_while(scanner, token):
    return Token(T_WHILE, MuddScanner.line_number, token)


def t_return(scanner, token):
    return Token(T_RETURN, MuddScanner.line_number, token)


def t_writeln(scanner, token):
    return Token(T_WRITELN, MuddScanner.line_number, token)


def t_write(scanner, token):
    return Token(T_WRITE, MuddScanner.line_number, token)


def t_read(scanner, token):
    return Token(T_READ, MuddScanner.line_number, token)


def t_semicol(scanner, token):
    return Token(T_SEMICOL, MuddScanner.line_number, token)


def t_comma(scanner, token):
    return Token(T_COMMA, MuddScanner.line_number, token)


def t_lbrack(scanner, token):
    return Token(T_LBRACK, MuddScanner.line_number, token)


def t_rbrack(scanner, token):
    return Token(T_RBRACK, MuddScanner.line_number, token)


def t_lcurly(scanner, token):
    return Token(T_LCURLY, MuddScanner.line_number, token)


def t_rcurly(scanner, token):
    return Token(T_RCURLY, MuddScanner.line_number, token)


def t_lparen(scanner, token):
    return Token(T_LPAREN, MuddScanner.line_number, token)


def t_rparen(scanner, token):
    return Token(T_RPAREN, MuddScanner.line_number, token)


def t_leq(scanner, token):
    return Token(T_LEQ, MuddScanner.line_number, token)


def t_les(scanner, token):
    return Token(T_LES, MuddScanner.line_number, token)


def t_equ(scanner, token):
    return Token(T_EQU, MuddScanner.line_number, token)


def t_neq(scanner, token):
    return Token(T_NEQ, MuddScanner.line_number, token)


def t_geq(scanner, token):
    return Token(T_GEQ, MuddScanner.line_number, token)


def t_gre(scanner, token):
    return Token(T_GRE, MuddScanner.line_number, token)


def t_plu(scanner, token):
    return Token(T_PLU, MuddScanner.line_number, token)


def t_min(scanner, token):
    return Token(T_MIN, MuddScanner.line_number, token)


def t_mul(scanner, token):
    return Token(T_MUL, MuddScanner.line_number, token)


def t_div(scanner, token):
    return Token(T_DIV, MuddScanner.line_number, token)


def t_mod(scanner, token):
    return Token(T_MOD, MuddScanner.line_number, token)


def t_and(scanner, token):
    return Token(T_AND, MuddScanner.line_number, token)


def t_eof(scanner, token):
    return Token(T_NEQ, MuddScanner.line_number, None)


def t_assign(scanner, token):
    return Token(T_ASSIGN, MuddScanner.line_number, token)


def new_line(scanner, token):
    MuddScanner.line_number += 1


def comment_new_line(scanner, token):
    MuddScanner.line_number += token.count('\n')
    return None


def comment_error(scanner, token):
    raise SyntaxError


token_patterns = [
    (r'/\*.*\*/', comment_new_line),
    (r'/\*.*', comment_error),
    (r'\n', new_line),
    (r'int', t_int),
    (r'void', t_void),
    (r'string', t_string),
    (r'if', t_if),
    (r'else', t_else),
    (r'while', t_while),
    (r'return', t_return),
    (r'writeln', t_writeln),
    (r'write', t_write),
    (r'read', t_read),
    (r';', t_semicol),
    (r',', t_comma),
    (r'\[', t_lbrack),
    (r'\]', t_rbrack),
    (r'\{', t_lcurly),
    (r'\}', t_rcurly),
    (r'\(', t_lparen),
    (r'\)', t_rparen),
    (r'<=', t_leq),
    (r'<', t_les),
    (r'==', t_equ),
    (r'!=', t_neq),
    (r'>=', t_geq),
    (r'>', t_gre),
    (r'\+', t_plu),
    (r'-', t_min),
    (r'\*', t_mul),
    (r'/', t_div),
    (r'%', t_mod),
    (r'&', t_and),
    (r'=', t_assign),
    (r'[a-zA-Z][a-zA-Z0-9_]*', t_id),
    (r'\d+', t_num),
    (r'\s+', None),  # ignore whitespace
    ]


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

    except SyntaxError:
        print('[SyntaxError] Unclosed comment exists.')
