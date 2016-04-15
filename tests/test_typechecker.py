from mudd import *
from mudd.typechecker import MuddTypeChecker


def set_up():
    checker = MuddTypeChecker('tests/bpl_files/test_typecheck_tdp.bpl')
    checker.top_down_pass()
    return checker


def test_top_down_pass():
    checker = set_up()
    print(checker.parse_tree)
    print(checker.symbols)
    assert True


def test_tdp_var_dec():
    checker = set_up()
    assert set(checker.symbols.keys()) == {
        'x', 'y', 'z', 'k', 'first', 'second', 'third'
        }
    gen = (symbol for symbol
           in checker.symbols.items()
           if symbol[0] in ['x', 'y', 'z']
           )
    for key, value in gen:
        assert value.kind == N_VAR_DEC


def traverse_tree(tree, node_list, check_tree):
        if tree.kind in node_list:
            check_tree(tree)
        elif hasattr(tree, 'children'):
            for child in tree.children:
                traverse_tree(child, node_list, check_tree)


def test_tdp_fun_dec_params_local_decs():
    checker = set_up()
    assert {'first', 'second', 'third'} - set(checker.symbols.keys()) == set()

    def check_tree(tree):
        if tree.children[1].value == 'first':
            assert {'x', 'y'} - set(
                tree.children[5].symbols.keys()
                ) == set()
        elif tree.children[1].value == 'second':
            assert {'a', 'b', 'c'} - set(
             tree.children[5].symbols.keys()
             ) == set()
        elif tree.children[1].value == 'third':
            assert tree.children[5].symbols == checker.symbols

    traverse_tree(checker.parse_tree, [N_FUN_DEC], check_tree)


def test_tdp_fun_dec_statement_list():
    checker = set_up()

    def check_tree(tree):
        if tree.children[0].kind == N_IF_STMT:
            assert {'inif'} - set(
                tree.children[0].children[4].children[0].symbols.keys()
                ) == set()
            assert {'inelse'} - set(
                tree.children[0].children[6].children[0].symbols.keys()
                ) == set()
        elif tree.children[0].kind == N_WHILE_STMT:
            assert {'inwhile'} - set(
                tree.children[0].children[4].children[0].symbols.keys()
             ) == set()

    traverse_tree(checker.parse_tree, [N_STATEMENT], check_tree)


def test_tdp_expression():
    checker = set_up()

    def check_tree(tree):
        if tree.children[0].kind == N_VAR:
            assert tree.children[0].children[0].kind == T_ID
            assert tree.children[0].children[0].value == 'x'
            var_dec = tree.children[0].children[0].declaration
            assert var_dec.children[0].children[0].kind == T_INT
            assert var_dec.children[1].kind == T_ID
            assert var_dec.children[1].value == 'x'
        elif tree.children[0].kind == N_COMP_EXP:
            assert True

    traverse_tree(checker.parse_tree, [N_EXPRESSION], check_tree)


def test_bottom_up_pass():
    checker = set_up()
    checker.bottom_up_pass()
    assert True
