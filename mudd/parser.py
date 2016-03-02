from .scanner import MuddScanner

from mudd import *


class ParseTree():
    """Parse Tree Node.

    """
    def __init__(self, kind):
        self.kind = kind
        self.children = []

    def __repr__(self):
        return '%d: %s' % (self.kind, self.children)


def program(scanner):
    parse_tree = ParseTree(N_PROGRAM)
    parse_tree.children.append(statement(scanner))
    return parse_tree


def statement(scanner):
    parse_tree = ParseTree(N_STATEMENT)
    parse_tree.children.append(expression_stmt(scanner))
    return parse_tree


def expression_stmt(scanner):
    parse_tree = ParseTree(N_EXPRESSION_STMT)
    parse_tree.children.append(expression(scanner))

    scanner.get_next_token()
    token = scanner.next_token
    if token.kind == T_SEMICOL:
        parse_tree.children.append(token)
    else:
        raise ParseError
    return parse_tree


def expression(scanner):
    parse_tree = ParseTree(N_EXPRESSION)
    token = scanner.next_token
    if token.kind == T_ID:
        parse_tree.children.append(token)
    else:
        raise ParseError
    return parse_tree


class MuddParser():
    """Recursive Descent Parser.

    """
    def __init__(self, filename):
        self.scanner = MuddScanner(filename)
        self.parse_tree = None

    def parse(self):
        self.scanner.get_next_token()
        self.parse_tree = program(self.scanner)
        self.scanner.get_next_token()
        if self.scanner.next_token.kind == T_EOF:
            print('Accept')
            return self.parse_tree
        else:
            print('Reject')
            raise ParseError


class ParseError(Exception):
    pass
