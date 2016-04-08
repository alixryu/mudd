from .parser import MuddParser

from mudd import *


class MuddTypeChecker():
    """Two-Pass Type Checker

    """
    def __init__(self, filename):
        self.parse_tree = MuddParser(filename).parse()
        # {T_ID.value : N_VAR_DEC | N_FUN_DEC}
        self.symbols = self.parse_tree.symbols
        # self.symbols[LOCAL_VARS] = {}

    def top_down_pass(self):
        self._tree_traversal(self.parse_tree)

    def _tree_traversal(self, tree):
        """Recursive depth-first-search tree traversal

        """
        if tree.kind in [N_FUN_DEC]:
            child_symbols = {
                t_id.value: tree for t_id in tree.children if t_id.kind == T_ID
                }
            self.symbols.update(child_symbols)
            tdp_fun_dec(tree, self.symbols)
            # TODO: find references in N_STATEMENT_LIST
        elif tree.kind in [N_VAR_DEC]:
            child_symbols = tdp_var_dec(tree)
            self.symbols.update(child_symbols)
        else:
            for child in tree.children:
                self.symbols.update(self._tree_traversal(child))

        return self.symbols

    def bottom_up_pass(self):
        pass


def tdp_var_dec(var_dec):
    child_symbols = {
        t_id.value: var_dec for t_id in var_dec.children if t_id.kind == T_ID
        }
    return child_symbols


def tdp_fun_dec(fun_dec, symbols):
    try:
        local_symbols = {}
        local_symbols.update(symbols)

        params = [
            child for child in fun_dec.children if child.kind == N_PARAMS
            ]
        params_symbols = tdp_params(params[0])
        local_symbols.update(params_symbols)

        compound_stmt = [
            child for child in fun_dec.children
            if child.kind == N_COMPOUND_STMT
            ]
        local_decs = compound_stmt[0].children[1]
        local_decs_symbols = tdp_local_decs(local_decs)
        local_symbols.update(local_decs_symbols)

        # apply symbols to COMPOUND_STMT
        compound_stmt[0].symbols.update(local_symbols)

    except IndexError:
        # TODO: raise error
        print('[ERROR] tdp_fun_dec')


def tdp_params(params):
    child = params.children[0]
    if child.kind == T_VOID:
        return {}
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


def tdp_local_decs(local_decs):
    local_symbols = {}
    if local_decs.children:
        local_symbols.update(tdp_local_decs(local_decs.children[0]))
        local_symbols.update(tdp_var_dec(local_decs.children[1]))
    return local_symbols


def update_symbols(child_symbols, parent_symbols):
    for r_k, r_v in parent_symbols.items():
        if r_k not in child_symbols.keys():
            child_symbols[r_k] = r_v


def add_symbol(symbols, key, value):
    symbols[key] = value
