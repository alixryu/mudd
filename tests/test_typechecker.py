from mudd import *
from mudd.typechecker import MuddTypeChecker, LOCAL_VARS


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
        'x', 'y', 'z', 'k', 'first', 'second', LOCAL_VARS
        }
    gen = (symbol for symbol
           in checker.symbols.items()
           if symbol[0] in ['x', 'y', 'z']
           )
    for key, value in gen:
        if key != LOCAL_VARS:
            assert value.kind == N_VAR_DEC


def test_tdp_fun_dec_local_decs():
    checker = MuddTypeChecker('tests/bpl_files/test_typecheck_tdp.bpl')
    checker.top_down_pass()
    assert LOCAL_VARS in checker.symbols.keys()
    assert set(checker.symbols[LOCAL_VARS].keys()) == {'first', 'second'}
    assert checker.symbols[LOCAL_VARS]['first'] is None
    assert set(
        checker.symbols[LOCAL_VARS]['second'].keys()
        ) == {'a', 'b', 'c'}
    for key, value in checker.symbols[LOCAL_VARS]['second'].items():
        assert value.kind == N_PARAM
    print(checker.symbols)
