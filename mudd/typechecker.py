from .parser import MuddParser

from mudd import *


LOCAL_VARS = 'locals'


class MuddTypeChecker():
    """Two-Pass Type Checker

    """
    def __init__(self, filename):
        self.parse_tree = MuddParser(filename).parse()
        # {T_ID.value : N_VAR_DEC | N_FUN_DEC}
        self.symbols = self.parse_tree.symbols
        self.symbols[LOCAL_VARS] = {}

    def top_down_pass(self):
        self._tree_traversal(self.parse_tree)

    def _tree_traversal(self, tree):
        """Recursive depth-first-search tree traversal

        """
        if tree.kind in [N_FUN_DEC]:
            child_symbols = {
                t_id.value: tree for t_id in tree.children if t_id.kind == T_ID
                }
            tree.symbols.update(child_symbols)
            tdp_fun_dec(tree, self.symbols)
            # TODO: find references in N_STATEMENT_LIST
        elif tree.kind in [N_VAR_DEC]:
            child_symbols = {
                t_id.value: tree for t_id in tree.children if t_id.kind == T_ID
                }
            tree.symbols.update(child_symbols)
        else:
            for child in tree.children:
                tree.symbols.update(self._tree_traversal(child))

        return tree.symbols

    def bottom_up_pass(self):
        pass


def tdp_fun_dec(fun_dec, symbols):
    params = [
        child for child in fun_dec.children if child.kind == N_PARAMS
        ]
    if len(params) == 1:
        func_symbols = tdp_params(params[0])
        child_symbols = {t_id.value: func_symbols
                         for t_id in fun_dec.children
                         if t_id.kind == T_ID
                         }
        symbols[LOCAL_VARS].update(child_symbols)
    else:
        # TODO: raise error
        print('[ERROR] tdp_fun_dec')


def tdp_params(params):
    if len(params.children) != 1:
        return None

    child = params.children[0]
    if child.kind == T_VOID:
        return None
    else:  # PARAM_LIST
        func_symbols = {}
        return tdp_param_list(child, func_symbols)


def tdp_param_list(param_list, func_symbols):
    for child in param_list.children:
        if child.kind == N_PARAM:
            child_symbols = {
                t_id.value: child
                for t_id in child.children
                if t_id.kind == T_ID
            }
            func_symbols.update(child_symbols)
        elif child.kind == N_PARAM_LIST:
            tdp_param_list(child, func_symbols)

    return func_symbols


def update_symbols(child_symbols, parent_symbols):
    for r_k, r_v in parent_symbols.items():
        if r_k not in child_symbols.keys():
            child_symbols[r_k] = r_v


def add_symbol(symbols, key, value):
    symbols[key] = value
