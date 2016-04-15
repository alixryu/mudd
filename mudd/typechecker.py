from .parser import MuddParser
from .scanner import Token

from mudd import *


debug = False


class MuddTypeChecker():
    """Two-Pass Type Checker

    """
    def __init__(self, filename, dbg=False):
        self.parse_tree = MuddParser(filename).parse()
        # {T_ID.value : N_VAR_DEC | N_FUN_DEC}
        self.symbols = self.parse_tree.symbols
        if dbg:
            global debug
            debug = True

    def top_down_pass(self):
        self._tdp_tree_traversal(self.parse_tree)

    def _tdp_tree_traversal(self, tree):
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
                self.symbols.update(self._tdp_tree_traversal(child))

        return self.symbols

    def bottom_up_pass(self):
        self._bup_tree_traversal(self.parse_tree)

    def _bup_tree_traversal(self, tree):
        """Recursive depth-first-search tree traversal

        """
        if tree.kind in [N_FUN_DEC]:
            bup_fun_dec(tree)
        else:
            if hasattr(tree, 'children'):
                for child in tree.children:
                    self._bup_tree_traversal(child)


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
        raise TypeCheckError(fun_dec)


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
    elif statement.kind == N_WHILE_STMT:
        expression = extract(statement, N_EXPRESSION)
        tdp_expression(expression, local_symbols)

        body_statement = extract(statement, N_STATEMENT)
        tdp_statement(body_statement, local_symbols)
    elif statement.kind in [N_RETURN_STMT, N_WRITE_STMT]:
        expression = extract(statement, N_EXPRESSION)
        tdp_expression(expression, local_symbols)
    elif statement.kind == N_COMPOUND_STMT:
        tdp_compound_stmt(statement, local_symbols)
    elif statement.kind == N_EXPRESSION_STMT:
        tdp_expression_stmt(statement, local_symbols)


def tdp_expression_stmt(expression_stmt, local_symbols):
    expression = extract(expression_stmt, N_EXPRESSION)
    if expression:
        tdp_expression(expression, local_symbols)


def tdp_expression(expression, local_symbols):
    tdp_find_reference(expression, local_symbols)


def tdp_find_reference(tree, local_symbols):
    try:
        if isinstance(tree, Token):
            if tree.kind == T_ID:
                declaration = local_symbols[tree.value]
                tree.declaration = declaration
                if debug:
                    print('Variable %s on line %d linked to declaration '
                          '%s on line %s' % (
                            tree.value,
                            tree.line_number,
                            extract(declaration, T_ID).value,
                            declaration.line_number
                            ))
        elif tree:
            for child in tree.children:
                tdp_find_reference(child, local_symbols)
    except KeyError:
        raise TypeCheckError(tree)


def bup_fun_dec(fun_dec):
    return_type = get_type(fun_dec)
    compound_stmt = extract(fun_dec, N_COMPOUND_STMT)
    bup_compound_stmt(compound_stmt, return_type)


def bup_statement_list(statement_list, return_type):
    if statement_list.children:
        # N_STATEMENT_LIST
        body_statement_list = extract(statement_list, N_STATEMENT_LIST)
        bup_statement_list(body_statement_list, return_type)

        # N_STATEMENT
        statement = extract(statement_list, N_STATEMENT)
        bup_statement(statement, return_type)


def bup_statement(statement, return_type):
    statement = statement.children[0]
    if statement.kind == N_EXPRESSION_STMT:
        bup_expression_stmt(statement)
    elif statement.kind == N_COMPOUND_STMT:
        bup_compound_stmt(statement, return_type)
    elif statement.kind == N_IF_STMT:
        bup_if_stmt(statement, return_type)
    elif statement.kind == N_WHILE_STMT:
        bup_while_stmt(statement, return_type)
    elif statement.kind == N_RETURN_STMT:
        bup_return_stmt(statement, return_type)
    elif statement.kind == N_WRITE_STMT:
        bup_write_stmt(statement)


def bup_while_stmt(while_stmt, return_type):
    expression = extract(while_stmt, N_EXPRESSION)
    expression_type = bup_expression(expression)

    if expression_type != Y_INT:
        raise TypeCheckError(while_stmt)

    statement = extract(while_stmt, N_STATEMENT)
    bup_statement(statement, return_type)


def bup_if_stmt(if_statement, return_type):
    expression = extract(if_statement, N_EXPRESSION)
    expression_type = bup_expression(expression)

    if expression_type != Y_INT:
        raise TypeCheckError(if_statement)

    statement = extract(if_statement, N_STATEMENT)
    bup_statement(statement, return_type)

    else_statement = extract(if_statement, N_STATEMENT, 1)
    if else_statement:
        bup_statement(else_statement, return_type)


def bup_return_stmt(return_stmt, return_type):
    expression = extract(return_stmt, N_EXPRESSION)
    if expression:
        if bup_expression(expression) != return_type:
            raise TypeCheckError(return_stmt)
    elif return_type != Y_VOID:  # and not expression
        raise TypeCheckError(return_stmt)


def bup_write_stmt(write_stmt):
    expression = extract(write_stmt, N_EXPRESSION)
    if expression:
        bup_expression(expression)


def bup_compound_stmt(compound_stmt, return_type):
    statement_list = extract(compound_stmt, N_STATEMENT_LIST)
    if statement_list:
        bup_statement_list(statement_list, return_type)


def bup_expression_stmt(expression_stmt):
    expression = extract(expression_stmt, N_EXPRESSION)
    if expression:
        bup_expression(expression)


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
            raise TypeCheckError(expression)

        expression.ttype = left_hand_type
    else:
        comp_exp = extract(expression, N_COMP_EXP)
        comp_exp_type = bup_comp_exp(comp_exp)

        expression.ttype = comp_exp_type

    if debug:
        print('Type %s assigned to expression in line %s' % (
            KIND_NAME[expression.ttype], expression.line_number
            ))

    return expression.ttype


def bup_comp_exp(comp_exp):
    e1 = extract(comp_exp, N_E)
    e2 = extract(comp_exp, N_E, 1)

    e1_type = bup_e(e1)

    if e2:
        e2_type = bup_e(e2)
        # Only int operations available
        if e1_type != Y_INT or e1_type != e2_type:
            raise TypeCheckError(comp_exp)

    return e1_type


def bup_e(e):
    body_e = extract(e, N_E)
    t = extract(e, N_T)

    t_type = bup_t(t)

    if body_e:
        body_e_type = bup_e(body_e)
        # Only int operations available
        if body_e_type != Y_INT or body_e_type != t_type:
            raise TypeCheckError(e)

    return t_type


def bup_t(t):
    body_t = extract(t, N_T)
    f = extract(t, N_F)

    f_type = bup_f(f)

    if body_t:
        body_t_type = bup_t(body_t)
        # Only int operations available
        if body_t_type != Y_INT or body_t_type != f_type:
            raise TypeCheckError(t)

    return f_type


def bup_f(f):
    factor = extract(f, N_FACTOR)
    if factor:
        factor_type = bup_factor(factor)
        if extract(f, T_MUL):  # pointer
            if factor_type == Y_INT:
                return Y_P_INT
            elif factor_type == Y_STR:
                return Y_P_STR
        elif extract(f, T_AND):  # address
            if factor_type == Y_INT:
                return Y_AD_INT
            elif factor_type == Y_STR:
                return Y_AD_STR
        else:
            return factor_type
    else:
        f_body = extract(f, N_F)
        body_f_type = bup_f(f_body)
        if body_f_type != Y_INT:
            raise TypeCheckError()
        return body_f_type


def bup_factor(factor):
    expression = extract(factor, N_EXPRESSION)
    fun_call = extract(factor, N_FUN_CALL)
    num = extract(factor, T_NUM)
    string = extract(factor, T_STRLIT)
    t_id = extract(factor, T_ID)
    # TODO: read(), <id>[N_EXPRESSION], *<id>
    t_read = extract(factor, T_READ)

    if expression and not t_id:
        return bup_expression(expression)
    elif fun_call:
        return bup_fun_call(fun_call)
    elif t_read:
        return get_type(t_read)  # Y_INT
    elif t_id:
        if expression:
            expression_type = bup_expression(expression)
            if expression_type != Y_INT:
                raise TypeCheckError(expression)
        return get_type(t_id.declaration)
    elif num:
        return get_type(num)  # Y_INT
    elif string:
        return get_type(string)  # Y_STRING
    else:
        # TODO: for debugging purposes
        return None


def bup_fun_call(fun_call):
    fun_dec = extract(fun_call, T_ID).declaration

    args_types = bup_args(fun_call)
    fun_dec_types = get_type_from_fun_dec(fun_dec)

    if args_types != fun_dec_types:
        raise TypeCheckError(fun_call)

    fun_type = get_type(fun_dec)
    return fun_type


def bup_args(fun_call):
    args = extract(fun_call, N_ARGS)
    arg_list = extract(args, N_ARG_LIST)

    if arg_list:
        return bup_arg_list(arg_list)
    else:
        return []


def bup_arg_list(arg_list):
    arg_list_type = []
    body_arg_list = extract(arg_list, N_ARG_LIST)
    if body_arg_list:
        arg_list_type.extend(bup_arg_list(body_arg_list))

    expression = extract(arg_list, N_EXPRESSION)
    expression_type = bup_expression(expression)
    arg_list_type.append(expression_type)

    return arg_list_type


def get_type_from_fun_dec(fun_dec):
    params = extract(fun_dec, N_PARAMS)
    param_list = extract(params, N_PARAM_LIST)

    if param_list:
        return bup_param_list(param_list)
    else:
        return []


def bup_param_list(param_list):
    param_list_type = []
    body_param_list = extract(param_list, N_PARAM_LIST)
    if body_param_list:
        param_list_type.extend(bup_param_list(body_param_list))

    param = extract(param_list, N_PARAM)
    param_type = get_type(param)
    param_list_type.append(param_type)

    return param_list_type


def get_type(var_dec):

    if var_dec.kind == T_NUM:
        return Y_INT
    elif var_dec.kind == T_STRLIT:
        return Y_STR

    type_identifier = extract(var_dec, N_TYPE_SPECIFIER)
    base_type = type_identifier.children[0].kind

    if extract(var_dec, T_MUL):  # POINTER
        if base_type == T_INT:
            return Y_P_INT
        elif base_type == T_STRING:
            return Y_P_STR
        else:
            raise TypeCheckError(var_dec)
    elif extract(var_dec, T_LBRACK):  # ARRAY
        if base_type == T_INT:
            return Y_A_INT
        elif base_type == T_STRING:
            return Y_A_STR
        else:
            raise TypeCheckError(var_dec)
    else:
        if base_type == T_INT:
            return Y_INT
        elif base_type == T_STRING:
            return Y_STR
        else:
            return Y_VOID


def extract(tree, non_terminal, index=0):
    result = [
        child for child in tree.children if child.kind == non_terminal
        ]
    return result[index] if result and len(result) > index else None


class TypeCheckError(Exception):
    def __init__(self, tree):
        self.tree = tree
        self.line_number = tree.line_number

    def __str__(self):
        return '[TypeCheckError] Error in %s in line %d' % (
            KIND_NAME[self.tree.kind], self.line_number
            )
