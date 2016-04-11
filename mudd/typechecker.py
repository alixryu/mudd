from .parser import MuddParser
from .scanner import Token

from mudd import *


class MuddTypeChecker():
    """Two-Pass Type Checker

    """
    def __init__(self, filename):
        self.parse_tree = MuddParser(filename).parse()
        # {T_ID.value : N_VAR_DEC | N_FUN_DEC}
        self.symbols = self.parse_tree.symbols

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

        # N_PARAMS
        params = extract(fun_dec, N_PARAMS)
        params_symbols = tdp_params(params)
        local_symbols.update(params_symbols)

        # N_COMPOUND_STMT
        compound_stmt = extract(fun_dec, N_COMPOUND_STMT)
        tdp_compound_stmt(compound_stmt, local_symbols)

    except IndexError:
        # TODO: raise error
        print('[ERROR] tdp_fun_dec')


def tdp_compound_stmt(compound_stmt, symbols):
    local_symbols = {}
    local_symbols.update(symbols)

    # N_LOCAL_DECS
    local_decs = compound_stmt.children[1]
    local_decs_symbols = tdp_local_decs(local_decs)
    local_symbols.update(local_decs_symbols)

    # apply symbols to COMPOUND_STMT
    compound_stmt.symbols.update(local_symbols)

    # N_STATEMENT_LIST
    tdp_statement_list(compound_stmt.children[2], compound_stmt.symbols)


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


def tdp_statement_list(statement_list, local_symbols):
    if statement_list.children:
        # N_STATEMENT_LIST
        body_statement_list = extract(statement_list, N_STATEMENT_LIST)
        tdp_statement_list(body_statement_list, local_symbols)

        # N_STATEMENT
        statement = extract(statement_list, N_STATEMENT)
        tdp_statement(statement, local_symbols)


def tdp_statement(statement, local_symbols):
    statement = statement.children[0]
    if statement.kind == N_IF_STMT:
        expression = extract(statement, N_EXPRESSION)
        tdp_expression(expression, local_symbols)

        body_statement = extract(statement, N_STATEMENT)
        tdp_statement(body_statement, local_symbols)

        else_statement = extract(statement, N_STATEMENT, 1)
        tdp_statement(else_statement, local_symbols)
        bup_if_stmt(statement)
    elif statement.kind == N_WHILE_STMT:
        expression = extract(statement, N_EXPRESSION)
        tdp_expression(expression, local_symbols)

        body_statement = extract(statement, N_STATEMENT)
        tdp_statement(body_statement, local_symbols)
        bup_while_stmt(statement)
    elif statement.kind in [N_RETURN_STMT, N_WRITE_STMT]:
        expression = extract(statement, N_EXPRESSION)
        tdp_expression(expression, local_symbols)
    elif statement.kind == N_COMPOUND_STMT:
        tdp_compound_stmt(statement, local_symbols)
    elif statement.kind == N_EXPRESSION_STMT:
        tdp_expression_stmt(statement, local_symbols)


def tdp_expression_stmt(expression_stmt, local_symbols):
    expression = extract(expression_stmt, N_EXPRESSION)
    tdp_expression(expression, local_symbols)


def tdp_expression(expression, local_symbols):
    tdp_find_reference(expression, local_symbols)


def tdp_find_reference(tree, local_symbols):
    try:
        if isinstance(tree, Token):
            if tree.kind == T_ID:
                declaration = local_symbols[tree.value]
                tree.declaration = declaration
        else:
            for child in tree.children:
                tdp_find_reference(child, local_symbols)
    except KeyError:
        # TODO: raise error
        print('[ERROR] tdp_find_reference')


def bup_statement(statement):
    pass


def bup_while_stmt(while_stmt):
    expression = extract(while_stmt, N_EXPRESSION)
    expression_type = bup_expression(expression)

    if expression_type != T_INT:
        raise TypeCheckError()

    statement = extract(while_stmt, N_STATEMENT)
    bup_statement(statement)


def bup_if_stmt(if_statement):
    expression = extract(if_statement, N_EXPRESSION)
    expression_type = bup_expression(expression)

    if expression_type != T_INT:
        raise TypeCheckError()

    statement = extract(if_statement, N_STATEMENT)
    bup_statement(statement)

    else_statement = extract(statement, N_STATEMENT, 1)
    bup_statement(else_statement)


def bup_expression(expression):
    if not hasattr(expression, 'ttype'):
        expression.ttype = None

    var = extract(expression, N_VAR)
    if var:
        t_id = extract(var, T_ID)
        left_hand_type = get_type(t_id.declaration)
        body_expression = extract(expression, N_EXPRESSION)
        right_hand_type = bup_expression(body_expression)

        if left_hand_type != right_hand_type:
            raise TypeCheckError()

        expression.ttype = left_hand_type

        return left_hand_type
    else:
        comp_exp = extract(expression, N_COMP_EXP)
        comp_exp_type = bup_comp_exp(comp_exp)

        expression.ttype = comp_exp_type

        return comp_exp_type


def bup_comp_exp(comp_exp):
    return T_INT


def get_type(var_dec):
    type_identifier = extract(var_dec, N_TYPE_SPECIFIER)
    the_type = type_identifier.children[0]
    return the_type


def extract(tree, non_terminal, index=0):
    result = [
        child for child in tree.children if child.kind == non_terminal
        ]
    return result[index] if result else None


class TypeCheckError(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return '[TypeCheckError] Error type checking'
