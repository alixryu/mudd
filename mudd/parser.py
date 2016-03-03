from .scanner import MuddScanner

from mudd import *


class ParseTree():
    """Parse Tree Node.

    """
    def __init__(self, kind):
        self.kind = kind
        self.children = []

    def __str__(self, level=0):
        ret = '  '*level+'%d\n' % (self.kind)
        for child in self.children:
            ret += child.__str__(level+1)
        return ret


def program(scanner):
    parse_tree = ParseTree(N_PROGRAM)
    parse_tree.children.append(statement(scanner))
    return parse_tree


def statement(scanner):
    parse_tree = ParseTree(N_STATEMENT)
    token = scanner.next_token
    if token.kind == T_LCURLY:
        parse_tree.children.append(compound_stmt(scanner))
    else:
        parse_tree.children.append(expression_stmt(scanner))
    return parse_tree


def expression_stmt(scanner):
    parse_tree = ParseTree(N_EXPRESSION_STMT)

    token = scanner.next_token
    if token.kind == T_SEMICOL:
        parse_tree.children.append(token)
    else:
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


def compound_stmt(scanner):
    parse_tree = ParseTree(N_COMPOUND_STMT)

    token = scanner.next_token
    # T_LCURLY
    if token.kind == T_LCURLY:
        parse_tree.children.append(token)
    else:
        raise ParseError

    # N_STATEMENT_LIST
    parse_tree.children.append(statement_list(scanner))

    token = scanner.next_token
    # T_RCURLY
    if token.kind == T_RCURLY:
        parse_tree.children.append(token)
    else:
        raise ParseError

    return parse_tree


def statement_list(scanner):
    parse_tree = ParseTree(N_STATEMENT_LIST)
    scanner.get_next_token()
    while not is_end_of_statement_list(scanner.next_token):
        parse_tree.children.append(statement(scanner))
        parse_tree_top = ParseTree(N_STATEMENT_LIST)
        parse_tree_top.children.append(parse_tree)
        parse_tree = parse_tree_top
        scanner.get_next_token()
    return parse_tree


def is_end_of_statement_list(token):
    end_of_statement_list_tokens = [T_RCURLY]
    return token.kind in end_of_statement_list_tokens


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
