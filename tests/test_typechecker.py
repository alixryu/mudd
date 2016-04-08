from mudd import *
from mudd.typechecker import MuddTypeChecker


def test_top_down_pass():
    checker = MuddTypeChecker('tests/bpl_files/test_typecheck_tdp.bpl')
    checker.top_down_pass()
    print(checker.parse_tree)
    print(checker.symbols)
    assert True


def test_tdp_var_dec():
    checker = MuddTypeChecker('tests/bpl_files/test_typecheck_tdp.bpl')
    checker.top_down_pass()
    assert set(checker.symbols.keys()) == {
        'x', 'y', 'z', 'k', 'first', 'second', 'third'
        }
    gen = (symbol for symbol
           in checker.symbols.items()
           if symbol[0] in ['x', 'y', 'z']
           )
    for key, value in gen:
        assert value.kind == N_VAR_DEC


def test_tdp_fun_dec_params_local_decs():
    checker = MuddTypeChecker('tests/bpl_files/test_typecheck_tdp.bpl')
    checker.top_down_pass()
    assert {'first', 'second', 'third'} - set(checker.symbols.keys()) == set()

    def traverse_tree(tree):
        if tree.kind in [N_FUN_DEC]:
            check_tree(tree)
        elif hasattr(tree, 'children'):
            for child in tree.children:
                traverse_tree(child)

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

    traverse_tree(checker.parse_tree)
