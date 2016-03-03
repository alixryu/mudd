from mudd import *
from mudd.parser import MuddParser, ParseTree


def test_parse_constructor():
    assert 'parse' in MuddParser.__dict__.keys()
    parser = MuddParser('factorial.bpl')
    test_parser_attributes = parser.__dict__.keys()
    assert 'scanner' in test_parser_attributes
    assert 'parse_tree' in test_parser_attributes


def test_parse_tree_constructor():
    parser = MuddParser('factorial.bpl')
    parser.scanner.get_next_token()
    token = parser.scanner.next_token
    parse_tree = ParseTree(token)
    assert 'children' in parse_tree.__dict__.keys()
    assert 'kind' in parse_tree.__dict__.keys()


def test_parse_single_id_statement():
    parser = MuddParser('tests/test_parse_single_id_statement.bpl')
    # test reaching accpet by T_EOF
    tree = parser.parse()
    assert tree is not None
    assert tree.kind == N_PROGRAM
    assert tree.children[0].kind == N_STATEMENT
    assert tree.children[0].children[0].kind == N_EXPRESSION_STMT
    assert tree.children[0].children[0].children[0].kind == N_EXPRESSION
    assert tree.children[0].children[0].children[0].children[0].kind == T_ID
    assert tree.children[0].children[0].children[1].kind == T_SEMICOL


def test_parse_statement_only_compound_statement():
    parser = MuddParser(
        'tests/test_parse_statement_only_compound_statement.bpl'
        )
    tree = parser.parse()
    print(tree)
    assert tree is not None
    assert tree.kind == N_PROGRAM
    assert tree.children[0].kind == N_STATEMENT
    assert tree.children[0].children[0].kind == N_COMPOUND_STMT
    assert tree.children[0].children[0].children[0].kind == T_LCURLY
    assert tree.children[0].children[0].children[-1].kind == T_RCURLY
    statement_list = tree.children[0].children[0].children[1].children[0]
    assert statement_list.kind == N_STATEMENT_LIST
    assert statement_list.children[0].kind == N_STATEMENT_LIST
    assert statement_list.children[1].kind == N_STATEMENT


def test_parse_while_statement():
    parser = MuddParser(
        'tests/test_parse_statement_only_compound_statement.bpl'
        )
    tree = parser.parse()
    print(tree)
    assert tree is not None
    assert tree.kind == N_PROGRAM
    assert tree.children[0].kind == N_STATEMENT
    assert tree.children[0].children[0].kind == N_COMPOUND_STMT
    assert tree.children[0].children[0].children[0].kind == T_LCURLY
    assert tree.children[0].children[0].children[-1].kind == T_RCURLY
    statement_list = tree.children[0].children[0].children[1].children[0]
    assert statement_list.kind == N_STATEMENT_LIST
    assert statement_list.children[1].kind == N_STATEMENT
    assert statement_list.children[1].children[0].kind == N_WHILE_STMT
    while_statement = statement_list.children[1].children[0]
    assert while_statement.children[0].kind == T_WHILE
    assert while_statement.children[1].kind == T_LPAREN
    assert while_statement.children[2].kind == N_EXPRESSION
    assert while_statement.children[3].kind == T_RPAREN
    assert while_statement.children[4].kind == N_STATEMENT
