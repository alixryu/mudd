from mudd import T_SEMICOL, T_ID, T_LCURLY, T_RCURLY
from mudd import N_PROGRAM, N_STATEMENT, N_EXPRESSION_STMT, N_EXPRESSION
from mudd import N_STATEMENT_LIST, N_COMPOUND_STMT
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
    statement_list = tree.children[0].children[0].children[1].children[0].kind
    assert statement_list == N_STATEMENT_LIST
