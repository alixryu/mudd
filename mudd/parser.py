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

    # N_STATEMENT
    parse_tree.children.append(statement(scanner))

    return parse_tree


def statement(scanner):
    parse_tree = ParseTree(N_STATEMENT)

    token = scanner.next_token
    if token.kind == T_LCURLY:
        parse_tree.children.append(compound_stmt(scanner))
    elif token.kind == T_IF:
        parse_tree.children.append(if_stmt(scanner))
    elif token.kind == T_WHILE:
        parse_tree.children.append(while_stmt(scanner))
    elif token.kind == T_RETURN:
        parse_tree.children.append(return_stmt(scanner))
    elif token.kind == T_WRITE or token.kind == T_WRITELN:
        parse_tree.children.append(write_stmt(scanner))
    else:
        parse_tree.children.append(expression_stmt(scanner))
    return parse_tree


def expression_stmt(scanner):
    parse_tree = ParseTree(N_EXPRESSION_STMT)

    if scanner.next_token.kind == T_SEMICOL:
        parse_tree.children.append(scanner.next_token)
    else:
        # N_EXPRESSION
        parse_tree.children.append(expression(scanner))
        scanner.get_next_token()

        # T_SEMICOL
        parse_tree.children.append(
            is_token_kind(T_SEMICOL, scanner.next_token)
            )

    scanner.get_next_token()

    return parse_tree


def expression(scanner):
    parse_tree = ParseTree(N_EXPRESSION)

    # T_ID
    parse_tree.children.append(is_token_kind(T_ID, scanner.next_token))

    return parse_tree


def compound_stmt(scanner):
    parse_tree = ParseTree(N_COMPOUND_STMT)

    # T_LCURLY
    parse_tree.children.append(is_token_kind(T_LCURLY, scanner.next_token))
    # N_STATEMENT_LIST
    parse_tree.children.append(statement_list(scanner))
    # T_RCURLY
    parse_tree.children.append(is_token_kind(T_RCURLY, scanner.next_token))
    scanner.get_next_token()

    return parse_tree


def statement_list(scanner):
    parse_tree = ParseTree(N_STATEMENT_LIST)
    scanner.get_next_token()
    while not _is_end_of_statement_list(scanner.next_token):
        parse_tree_top = ParseTree(N_STATEMENT_LIST)
        parse_tree_top.children.append(parse_tree)
        parse_tree = parse_tree_top
        parse_tree.children.append(statement(scanner))

    return parse_tree


def _is_end_of_statement_list(token):
    end_of_statement_list_tokens = [T_RCURLY]
    return token.kind in end_of_statement_list_tokens


def while_stmt(scanner):
    parse_tree = ParseTree(N_WHILE_STMT)

    # T_WHILE
    parse_tree.children.append(is_token_kind(T_WHILE, scanner.next_token))
    scanner.get_next_token()
    # T_LPAREN
    parse_tree.children.append(is_token_kind(T_LPAREN, scanner.next_token))
    scanner.get_next_token()
    # N_EXPRESSION
    parse_tree.children.append(expression(scanner))
    scanner.get_next_token()
    # T_RPAREN
    parse_tree.children.append(is_token_kind(T_RPAREN, scanner.next_token))
    scanner.get_next_token()
    # N_STATEMENT
    parse_tree.children.append(statement(scanner))
    # scanner.get_next_token()

    return parse_tree


def if_stmt(scanner):
    parse_tree = ParseTree(N_IF_STMT)

    # T_IF
    parse_tree.children.append(is_token_kind(T_IF, scanner.next_token))
    scanner.get_next_token()
    # T_LPAREN
    parse_tree.children.append(is_token_kind(T_LPAREN, scanner.next_token))
    scanner.get_next_token()
    # N_EXPRESSION
    parse_tree.children.append(expression(scanner))
    scanner.get_next_token()
    # T_RPAREN
    parse_tree.children.append(is_token_kind(T_RPAREN, scanner.next_token))
    scanner.get_next_token()
    # N_STATEMENT
    parse_tree.children.append(statement(scanner))
    # scanner.get_next_token()

    # T_ELSE
    if scanner.next_token.kind == T_ELSE:
        parse_tree.children.append(scanner.next_token)
        scanner.get_next_token()
        # N_STATEMENT
        parse_tree.children.append(statement(scanner))

    return parse_tree


def return_stmt(scanner):
    parse_tree = ParseTree(N_RETURN_STMT)

    # T_RETURN
    parse_tree.children.append(is_token_kind(T_RETURN, scanner.next_token))
    scanner.get_next_token()

    if scanner.next_token.kind == T_SEMICOL:
        # T_SEMICOL
        parse_tree.children.append(
            is_token_kind(T_SEMICOL, scanner.next_token)
            )
    else:
        # N_EXPRESSION
        parse_tree.children.append(expression(scanner))
        scanner.get_next_token()
        # T_SEMICOL
        parse_tree.children.append(
            is_token_kind(T_SEMICOL, scanner.next_token)
            )

    scanner.get_next_token()

    return parse_tree


def write_stmt(scanner):
    parse_tree = ParseTree(N_RETURN_STMT)

    if scanner.next_token.kind == T_WRITE:
        # T_WRITE
        parse_tree.children.append(is_token_kind(T_WRITE, scanner.next_token))
        scanner.get_next_token()
        # T_LPAREN
        parse_tree.children.append(is_token_kind(T_LPAREN, scanner.next_token))
        scanner.get_next_token()
        # N_EXPRESSION
        parse_tree.children.append(expression(scanner))
        scanner.get_next_token()
        # T_RPAREN
        parse_tree.children.append(is_token_kind(T_RPAREN, scanner.next_token))
        scanner.get_next_token()
        # T_SEMICOL
        parse_tree.children.append(is_token_kind(T_SEMICOL, scanner.next_token))
        scanner.get_next_token()

    elif scanner.next_token.kind == T_WRITELN:
        # T_WRITELN
        parse_tree.children.append(
            is_token_kind(T_WRITELN, scanner.next_token)
            )
        scanner.get_next_token()
        # T_LPAREN
        parse_tree.children.append(is_token_kind(T_LPAREN, scanner.next_token))
        scanner.get_next_token()
        # T_RPAREN
        parse_tree.children.append(is_token_kind(T_RPAREN, scanner.next_token))
        scanner.get_next_token()
        # T_SEMICOL
        parse_tree.children.append(is_token_kind(T_SEMICOL, scanner.next_token))
        scanner.get_next_token()

    return parse_tree


def is_token_kind(token_kind, token):
    if token.kind == token_kind:
        return token
    else:
        raise ParseError


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
