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

'''
def test_parse_single_id_expression():
    parser = MuddParser('tests/test_parse_single_id_statement.bpl')
    tree = parser.parse()
    assert tree.kind == N_PROGRAM
    assert tree.children[0].kind == N_DECLARATION_LIST
    assert tree.children[0].children[0].kind == N_DECLARATION
    assert tree.children[0].children[0].children[0].kind == N_FUN_DEC
    fun_dec = tree.children[0].children[0].children[0]
    assert fun_dec.children[5].kind == N_COMPOUND_STMT
    assert fun_dec.children[5].children[1].kind == N_STATEMENT_LIST
    assert fun_dec.children[5].children[1].children[1].kind == N_STATEMENT
    statement = fun_dec.children[5].children[1].children[1]
    assert statement.children[0].kind == N_EXPRESSION_STMT
    assert statement.children[0].children[0].kind == N_EXPRESSION
    assert statement.children[0].children[0].children[0].kind == T_ID
    assert statement.children[0].children[1].kind == T_SEMICOL
'''


def test_parse_statement_only_compound_statement():
    parser = MuddParser(
        'tests/test_parse_statement_only_compound_statement.bpl'
        )
    tree = parser.parse()

    assert tree.kind == N_PROGRAM
    assert tree.children[0].kind == N_DECLARATION_LIST
    assert tree.children[0].children[0].kind == N_DECLARATION
    assert tree.children[0].children[0].children[0].kind == N_FUN_DEC
    fun_dec = tree.children[0].children[0].children[0]
    assert fun_dec.children[5].kind == N_COMPOUND_STMT
    compound_stmt = fun_dec.children[5]
    assert compound_stmt.children[0].kind == T_LCURLY
    assert compound_stmt.children[1].kind == N_LOCAL_DECS
    assert compound_stmt.children[2].kind == N_STATEMENT_LIST
    assert compound_stmt.children[2].children[0].kind == N_STATEMENT_LIST
    assert compound_stmt.children[2].children[1].kind == N_STATEMENT
    assert compound_stmt.children[3].kind == T_RCURLY


def test_parse_while_statement():
    parser = MuddParser(
        'tests/test_parse_statement_only_compound_statement.bpl'
        )
    tree = parser.parse()
    compound_stmt = tree.children[0].children[0].children[0].children[5]
    while_statement = compound_stmt.children[2].children[1].children[0]
    assert while_statement.children[0].kind == T_WHILE
    assert while_statement.children[1].kind == T_LPAREN
    assert while_statement.children[2].kind == N_EXPRESSION
    assert while_statement.children[3].kind == T_RPAREN
    assert while_statement.children[4].kind == N_STATEMENT
    print(while_statement)


def test_parse_if_statement():
    parser = MuddParser(
        'tests/test_parse_statement_only_compound_statement.bpl'
        )
    tree = parser.parse()
    compound_stmt = tree.children[0].children[0].children[0].children[5]
    if_statement = compound_stmt.children[
        2].children[0].children[0].children[1].children[0]
    assert if_statement.children[0].kind == T_IF
    assert if_statement.children[1].kind == T_LPAREN
    assert if_statement.children[2].kind == N_EXPRESSION
    assert if_statement.children[3].kind == T_RPAREN
    assert if_statement.children[4].kind == N_STATEMENT
    if_else_statement = compound_stmt.children[
        2].children[0].children[1].children[0]
    assert if_else_statement.children[0].kind == T_IF
    assert if_else_statement.children[1].kind == T_LPAREN
    assert if_else_statement.children[2].kind == N_EXPRESSION
    assert if_else_statement.children[3].kind == T_RPAREN
    assert if_else_statement.children[4].kind == N_STATEMENT
    assert if_else_statement.children[5].kind == T_ELSE
    assert if_else_statement.children[6].kind == N_STATEMENT
    print(if_statement)
    print(if_else_statement)


def test_parse_return_statement():
    parser = MuddParser(
        'tests/test_parse_statement_only_compound_statement.bpl'
        )
    tree = parser.parse()
    compound_stmt = tree.children[0].children[0].children[0].children[5]
    return_statement = compound_stmt.children[
        2].children[0].children[0].children[0].children[1].children[0]
    assert return_statement.children[0].kind == T_RETURN
    assert return_statement.children[1].kind == T_SEMICOL
    return_statement2 = compound_stmt.children[
        2].children[0].children[0].children[0].children[
            0].children[1].children[0]
    assert return_statement2.children[0].kind == T_RETURN
    assert return_statement2.children[1].kind == N_EXPRESSION
    assert return_statement2.children[2].kind == T_SEMICOL
    print(return_statement)
    print(return_statement2)


def test_parse_write_statement():
    parser = MuddParser(
        'tests/test_parse_statement_only_compound_statement.bpl'
        )
    tree = parser.parse()
    compound_stmt = tree.children[0].children[0].children[0].children[5]
    write_statement = compound_stmt.children[
        2].children[0].children[0].children[0].children[
            0].children[0].children[1].children[0]
    assert write_statement.children[0].kind == T_WRITE
    assert write_statement.children[1].kind == T_LPAREN
    assert write_statement.children[2].kind == N_EXPRESSION
    assert write_statement.children[3].kind == T_RPAREN
    assert write_statement.children[4].kind == T_SEMICOL
    writeln_statement = compound_stmt.children[
        2].children[0].children[0].children[0].children[
            0].children[0].children[0].children[1].children[0]
    assert writeln_statement.children[0].kind == T_WRITELN
    assert writeln_statement.children[1].kind == T_LPAREN
    assert writeln_statement.children[2].kind == T_RPAREN
    assert writeln_statement.children[3].kind == T_SEMICOL
    print(write_statement)
    print(writeln_statement)


def test_parse_declaration():
    parser = MuddParser(
        'tests/test_parse_variable_declaration.bpl'
        )
    tree = parser.parse()
    assert tree.kind == N_PROGRAM
    assert tree.children[0].kind == N_DECLARATION_LIST
    assert tree.children[0].children[0].kind == N_DECLARATION_LIST
    assert tree.children[0].children[1].kind == N_DECLARATION
    print(tree)


def test_parse_var_dec():
    parser = MuddParser(
        'tests/test_parse_variable_declaration.bpl'
        )
    tree = parser.parse()
    assert tree.kind == N_PROGRAM
    assert tree.children[0].kind == N_DECLARATION_LIST
    assert tree.children[0].children[0].kind == N_DECLARATION_LIST
    assert tree.children[0].children[1].kind == N_DECLARATION
    declaration1 = tree.children[0].children[1]
    assert declaration1.children[0].kind == N_VAR_DEC
    assert declaration1.children[0].children[0].kind == N_TYPE_SPECIFIER
    assert declaration1.children[0].children[1].kind == T_ID
    assert declaration1.children[0].children[2].kind == T_SEMICOL
    declaration2 = tree.children[0].children[0].children[1]
    assert declaration2.children[0].kind == N_VAR_DEC
    assert declaration2.children[0].children[0].kind == N_TYPE_SPECIFIER
    assert declaration2.children[0].children[1].kind == T_MUL
    assert declaration2.children[0].children[2].kind == T_ID
    assert declaration2.children[0].children[3].kind == T_SEMICOL
    declaration3 = tree.children[0].children[0].children[0].children[0]
    assert declaration3.children[0].kind == N_VAR_DEC
    assert declaration3.children[0].children[0].kind == N_TYPE_SPECIFIER
    assert declaration3.children[0].children[1].kind == T_ID
    assert declaration3.children[0].children[2].kind == T_LBRACK
    assert declaration3.children[0].children[3].kind == T_NUM
    assert declaration3.children[0].children[4].kind == T_RBRACK
    assert declaration3.children[0].children[5].kind == T_SEMICOL
    print(declaration1)
    print(declaration2)
    print(declaration3)


def test_parse_fun_dec():
    parser = MuddParser(
        'tests/test_parse_function_declaration.bpl'
        )
    tree = parser.parse()
    assert tree.kind == N_PROGRAM
    assert tree.children[0].kind == N_DECLARATION_LIST
    assert tree.children[0].children[0].kind == N_DECLARATION_LIST
    assert tree.children[0].children[1].kind == N_DECLARATION
    declaration1 = tree.children[0].children[1]
    assert declaration1.children[0].kind == N_FUN_DEC
    assert declaration1.children[0].children[0].kind == N_TYPE_SPECIFIER
    assert declaration1.children[0].children[1].kind == T_ID
    assert declaration1.children[0].children[2].kind == T_LPAREN
    assert declaration1.children[0].children[3].kind == N_PARAMS
    assert declaration1.children[0].children[4].kind == T_RPAREN
    assert declaration1.children[0].children[5].kind == N_COMPOUND_STMT
    void_params = declaration1.children[0].children[3]
    assert void_params.children[0].kind == T_VOID
    declaration2 = tree.children[0].children[0].children[0]
    param_list_params = declaration2.children[0].children[3]
    assert param_list_params.children[0].kind == N_PARAM_LIST
    array_param = param_list_params.children[0].children[2]
    assert array_param.children[0].kind == N_TYPE_SPECIFIER
    assert array_param.children[1].kind == T_ID
    assert array_param.children[2].kind == T_LBRACK
    assert array_param.children[3].kind == T_RBRACK
    pointer_param = param_list_params.children[0].children[0].children[2]
    assert pointer_param.children[0].kind == N_TYPE_SPECIFIER
    assert pointer_param.children[1].kind == T_MUL
    assert pointer_param.children[2].kind == T_ID
    id_param = param_list_params.children[
        0].children[0].children[0].children[0]
    assert id_param.children[0].kind == N_TYPE_SPECIFIER
    assert id_param.children[1].kind == T_ID
    print(void_params)
    print(array_param)
    print(pointer_param)
    print(id_param)


def test_parse_expression():
    parser = MuddParser(
        'tests/test_parse_expression.bpl'
        )
    tree = parser.parse()
    fun_dec = tree.children[0].children[0].children[0]
    statement_list = fun_dec.children[5].children[2]
    statement1 = statement_list.children[1]
    expression1 = statement1.children[0].children[0]
    assert expression1.children[0].kind == N_VAR
    assert expression1.children[0].children[0].kind == T_MUL
    assert expression1.children[0].children[1].kind == T_ID
    assert expression1.children[1].kind == T_ASSIGN
    assert expression1.children[2].kind == N_EXPRESSION
    statement2 = statement_list.children[0].children[1]
    expression2 = statement2.children[0].children[0]
    assert expression2.children[0].kind == N_VAR
    assert expression2.children[0].children[0].kind == T_ID
    assert expression2.children[0].children[2].kind == N_EXPRESSION
    assert expression2.children[1].kind == T_ASSIGN
    assert expression2.children[2].kind == N_EXPRESSION
    statement3 = statement_list.children[0].children[0].children[1]
    expression3 = statement3.children[0].children[0]
    assert expression3.children[0].kind == N_VAR
    assert expression3.children[0].children[0].kind == T_ID
    assert expression3.children[1].kind == T_ASSIGN
    assert expression3.children[2].kind == N_EXPRESSION
    print(expression1)
    print(expression2)
    print(expression3)


def test_parse_comp_exp():
    parser = MuddParser(
        'tests/test_parse_expression.bpl'
        )
    tree = parser.parse()
    fun_dec = tree.children[0].children[0].children[0]
    base_statement_list = fun_dec.children[5].children[2]
    statement_list = base_statement_list.children[0].children[0].children[0]
    statement = statement_list.children[1]
    expression = statement.children[0].children[0]
    comp_exp = expression.children[0]
    assert comp_exp.kind == N_COMP_EXP


def test_parse_fun_call():
    parser = MuddParser(
        'tests/test_parse_expression.bpl'
        )
    tree = parser.parse()
    fun_dec = tree.children[0].children[0].children[0]
    base_statement_list = fun_dec.children[5].children[2]
    statement_list = base_statement_list.children[
        0].children[0].children[0].children[0]
    statement = statement_list.children[1]
    expression = statement.children[0].children[0]
    comp_exp = expression.children[0]
    fun_call = comp_exp.children[
        0].children[0].children[0].children[0].children[0]
    assert fun_call.kind == N_FUN_CALL
    assert fun_call.children[0].kind == T_ID
    assert fun_call.children[2].kind == N_ARGS
    arg_list = fun_call.children[2].children[0]
    assert arg_list.children[2].kind == N_EXPRESSION
    assert arg_list.children[0].children[0].kind == N_EXPRESSION
    print(fun_call)


def test_parse_local_decs():
    parser = MuddParser(
        'tests/test_parse_local_decs.bpl'
        )
    tree = parser.parse()
    fun_dec1 = tree.children[0].children[1].children[0]
    assert fun_dec1.children[5].kind == N_COMPOUND_STMT
    compound_stmt1 = fun_dec1.children[5]
    local_decs1 = compound_stmt1.children[1]
    assert not local_decs1.children
    fun_dec2 = tree.children[0].children[0].children[0].children[0]
    assert fun_dec2.children[5].kind == N_COMPOUND_STMT
    compound_stmt2 = fun_dec2.children[5]
    local_decs2 = compound_stmt2.children[1]
    assert local_decs2.children[1].kind == N_VAR_DEC
    assert local_decs2.children[0].children[1].kind == N_VAR_DEC
    print(local_decs1)
    print(local_decs2)
