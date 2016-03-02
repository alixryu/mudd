from mudd import T_SEMICOL, T_ID
from mudd import N_PROGRAM, N_STATEMENT, N_EXPRESSION_STMT, N_EXPRESSION
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


def test_parse():
    parser = MuddParser('test_parser.bpl')
    # test reaching accpet by T_EOF
    tree = parser.parse()
    assert tree is not None
    assert tree.kind == N_PROGRAM
    assert tree.children[0].kind == N_STATEMENT
    assert tree.children[0].children[0].kind == N_EXPRESSION_STMT
    assert tree.children[0].children[0].children[0].kind == N_EXPRESSION
    assert tree.children[0].children[0].children[0].children[0].kind == T_ID
    assert tree.children[0].children[0].children[1].kind == T_SEMICOL
