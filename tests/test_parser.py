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
    parse_tree = ParseTree(token, 1)
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
    assert tree is not None
    assert tree.kind == N_PROGRAM
    assert tree.children[0].kind == N_STATEMENT
    assert tree.children[0].children[0].kind == N_COMPOUND_STMT
    assert tree.children[0].children[0].children[0].kind == T_LCURLY
    assert tree.children[0].children[0].children[-1].kind == T_RCURLY
    statement_list = tree.children[0].children[0].children[1]
    assert statement_list.kind == N_STATEMENT_LIST
    assert statement_list.children[0].kind == N_STATEMENT_LIST
    assert statement_list.children[1].kind == N_STATEMENT


def test_parse_while_statement():
    parser = MuddParser(
        'tests/test_parse_statement_only_compound_statement.bpl'
        )
    tree = parser.parse()
    statement_list = tree.children[0].children[0].children[1]
    while_statement_list = statement_list.children[0].children[0].children[0]
    while_statement = while_statement_list.children[1].children[0]
    assert while_statement.children[0].kind == T_WHILE
    assert while_statement.children[1].kind == T_LPAREN
    assert while_statement.children[2].kind == N_EXPRESSION
    assert while_statement.children[3].kind == T_RPAREN
    assert while_statement.children[4].kind == N_STATEMENT
    print(while_statement_list.children[1])


def test_parse_if_statement():
    parser = MuddParser(
        'tests/test_parse_statement_only_compound_statement.bpl'
        )
    tree = parser.parse()
    statement_list = tree.children[0].children[0].children[1]
    while_statement_list = statement_list.children[0].children[0].children[0]
    if_statement_list = while_statement_list.children[0].children[0]
    if_statement = if_statement_list.children[1].children[0]
    assert if_statement.children[0].kind == T_IF
    assert if_statement.children[1].kind == T_LPAREN
    assert if_statement.children[2].kind == N_EXPRESSION
    assert if_statement.children[3].kind == T_RPAREN
    assert if_statement.children[4].kind == N_STATEMENT
    if_else_statement_list = while_statement_list.children[0]
    if_else_statement = if_else_statement_list.children[1].children[0]
    assert if_else_statement.children[0].kind == T_IF
    assert if_else_statement.children[1].kind == T_LPAREN
    assert if_else_statement.children[2].kind == N_EXPRESSION
    assert if_else_statement.children[3].kind == T_RPAREN
    assert if_else_statement.children[4].kind == N_STATEMENT
    assert if_else_statement.children[5].kind == T_ELSE
    assert if_else_statement.children[6].kind == N_STATEMENT
    print(if_statement_list.children[1])
    print(if_else_statement_list.children[1])


def test_parse_return_statement():
    parser = MuddParser(
        'tests/test_parse_statement_only_compound_statement.bpl'
        )
    tree = parser.parse()
    statement_list = tree.children[0].children[0].children[1]
    while_statement_list = statement_list.children[0].children[0].children[0]
    if_statement_list = while_statement_list.children[0].children[0]
    return_statement_list = if_statement_list.children[0]
    return_statement = return_statement_list.children[1].children[0]
    assert return_statement.children[0].kind == T_RETURN
    assert return_statement.children[1].kind == T_SEMICOL
    return_statement_list2 = if_statement_list.children[0].children[0]
    return_statement2 = return_statement_list2.children[1].children[0]
    assert return_statement2.children[0].kind == T_RETURN
    assert return_statement2.children[1].kind == N_EXPRESSION
    assert return_statement2.children[2].kind == T_SEMICOL
    print(return_statement_list.children[1])
    print(return_statement_list2.children[1])


def test_parse_write_statement():
    parser = MuddParser(
        'tests/test_parse_statement_only_compound_statement.bpl'
        )
    tree = parser.parse()
    statement_list = tree.children[0].children[0].children[1]
    while_statement_list = statement_list.children[0].children[0].children[0]
    if_statement_list = while_statement_list.children[0].children[0]
    return_statement_list2 = if_statement_list.children[0].children[0]
    write_statement_list = return_statement_list2.children[0]
    write_statement = write_statement_list.children[1].children[0]
    assert write_statement.children[0].kind == T_WRITE
    assert write_statement.children[1].kind == T_LPAREN
    assert write_statement.children[2].kind == N_EXPRESSION
    assert write_statement.children[3].kind == T_RPAREN
    assert write_statement.children[4].kind == T_SEMICOL
    writeln_statement_list = return_statement_list2.children[0].children[0]
    writeln_statement = writeln_statement_list.children[1].children[0]
    assert writeln_statement.children[0].kind == T_WRITELN
    assert writeln_statement.children[1].kind == T_LPAREN
    assert writeln_statement.children[2].kind == T_RPAREN
    assert writeln_statement.children[3].kind == T_SEMICOL
    print(write_statement_list.children[1])
    print(writeln_statement_list.children[1])
