from .scanner import MuddScanner

from mudd import *


class ParseTree():
    """Parse Tree Node.

    """
    def __init__(self, kind, line_number):
        self.kind = kind
        self.line_number = line_number
        self.children = []
        self.symbols = {}

    def __str__(self, level=0):
        ret = '  '*level+'%s\tLine: %d\n' % (
            KIND_NAME[self.kind], self.line_number
            )
        for child in self.children:
            ret += child.__str__(level+1)
        return ret

    def add(self, parse_tree):
        self.children.append(parse_tree)


def program(scanner):
    parse_tree = ParseTree(N_PROGRAM, scanner.get_line_number())

    # N_DECLARATION_LIST
    parse_tree.add(declaration_list(scanner))

    return parse_tree


def declaration_list(scanner):
    parse_tree = ParseTree(N_DECLARATION_LIST, scanner.get_line_number())

    # N_DECLARATION (minimum 1 declaration required)
    parse_tree.add(declaration(scanner))
    while not _is_end_of_declaration_list(scanner.next_token):
        parse_tree_top = ParseTree(
            N_DECLARATION_LIST, parse_tree.line_number
            )
        parse_tree_top.children.append(parse_tree)
        parse_tree = parse_tree_top
        parse_tree.add(declaration(scanner))

    return parse_tree


def _is_end_of_declaration_list(token):
    end_of_declaration_list_tokens = [T_EOF]
    return token.kind in end_of_declaration_list_tokens


def declaration(scanner):
    parse_tree = ParseTree(N_DECLARATION, scanner.get_line_number())

    scanner.set_backtrack_index()
    # N_VAR_DEC
    parse_tree_var_dec = var_dec(scanner, parse_error=False)

    if parse_tree_var_dec:
        parse_tree.add(parse_tree_var_dec)
        scanner.unset_backtrack_index()
    else:
        scanner.backtrack()
        parse_tree.add(fun_dec(scanner))

    return parse_tree


def var_dec(scanner, parse_error=True):
    try:
        parse_tree = ParseTree(N_VAR_DEC, scanner.get_line_number())
        # N_TYPE_SPECIFIER
        parse_tree.add(type_specifier(scanner))
        is_pointer = False
        if scanner.next_token.kind == T_MUL:
            is_pointer = True
            # T_MUL (pointer)
            parse_tree.add(
                is_token_kind(
                    scanner.next_token, T_MUL, parse_error=parse_error
                    )
                )
            scanner.get_next_token()
        # T_ID
        parse_tree.add(
            is_token_kind(
                scanner.next_token, T_ID, parse_error=parse_error
                )
            )
        scanner.get_next_token()

        if scanner.next_token.kind == T_LBRACK and not is_pointer:
            # T_LBRACK
            parse_tree.add(
                is_token_kind(
                    scanner.next_token, T_LBRACK, parse_error=parse_error
                    )
                )
            scanner.get_next_token()
            # T_NUM
            parse_tree.add(
                is_token_kind(
                    scanner.next_token, T_NUM, parse_error=parse_error
                    )
                )
            scanner.get_next_token()
            # T_RBRACK
            parse_tree.add(
                is_token_kind(
                    scanner.next_token, T_RBRACK, parse_error=parse_error
                    )
                )
            scanner.get_next_token()

        # T_SEMICOL
        parse_tree.add(
            is_token_kind(
                scanner.next_token, T_SEMICOL, parse_error=parse_error
                )
            )
        scanner.get_next_token()
        return parse_tree
    except BackTrackError:
        return None


def fun_dec(scanner):
    parse_tree = ParseTree(N_FUN_DEC, scanner.get_line_number())

    # N_TYPE_SPECIFIER
    parse_tree.add(type_specifier(scanner))
    # T_ID
    parse_tree.add(is_token_kind(scanner.next_token, T_ID))
    scanner.get_next_token()
    # T_LPAREN
    parse_tree.add(
        is_token_kind(scanner.next_token, T_LPAREN)
        )
    scanner.get_next_token()
    # N_PARAMS
    parse_tree.add(
        params(scanner)
        )
    # T_RPAREN
    parse_tree.add(
        is_token_kind(scanner.next_token, T_RPAREN)
        )
    scanner.get_next_token()
    # N_COMPOUND_STMT
    parse_tree.add(compound_stmt(scanner))

    return parse_tree


def type_specifier(scanner):
    parse_tree = ParseTree(N_TYPE_SPECIFIER, scanner.get_line_number())

    if scanner.next_token.kind == T_INT:
        parse_tree.add(is_token_kind(scanner.next_token, T_INT))
    elif scanner.next_token.kind == T_VOID:
        parse_tree.add(is_token_kind(scanner.next_token, T_VOID))
    else:
        parse_tree.add(is_token_kind(scanner.next_token, T_STRING))
    scanner.get_next_token()

    return parse_tree


def params(scanner):
    parse_tree = ParseTree(N_PARAMS, scanner.get_line_number())

    if scanner.next_token.kind == T_VOID:
        parse_tree.add(is_token_kind(scanner.next_token, T_VOID))
        scanner.get_next_token()
    else:
        parse_tree.add(param_list(scanner))

    return parse_tree


def param_list(scanner):
    parse_tree = ParseTree(N_PARAM_LIST, scanner.get_line_number())

    # N_PARAM (minimum 1 parameter required)
    parse_tree.add(param(scanner))
    while not _is_end_of_param_list(scanner.next_token):
        parse_tree_top = ParseTree(N_PARAM_LIST, parse_tree.line_number)
        parse_tree_top.children.append(parse_tree)
        parse_tree = parse_tree_top
        parse_tree.add(is_token_kind(scanner.next_token, T_COMMA))
        scanner.get_next_token()
        parse_tree.add(param(scanner))

    return parse_tree


def _is_end_of_param_list(token):
    end_of_param_list_tokens = [T_RPAREN]
    return token.kind in end_of_param_list_tokens


def param(scanner):
    parse_tree = ParseTree(N_PARAM, scanner.get_line_number())

    # N_TYPE_SPECIFIER
    parse_tree.add(type_specifier(scanner))

    if scanner.next_token.kind == T_MUL:
        # T_MUL (pointer)
        parse_tree.add(is_token_kind(scanner.next_token, T_MUL))
        scanner.get_next_token()
        # T_ID
        parse_tree.add(is_token_kind(scanner.next_token, T_ID))
        scanner.get_next_token()
    else:
        # T_ID
        parse_tree.add(is_token_kind(scanner.next_token, T_ID))
        scanner.get_next_token()
        if scanner.next_token.kind == T_LBRACK:
            # T_LBRACK
            parse_tree.add(
                is_token_kind(scanner.next_token, T_LBRACK)
                )
            scanner.get_next_token()
            # T_RBRACK
            parse_tree.add(
                is_token_kind(scanner.next_token, T_RBRACK)
                )
            scanner.get_next_token()
        # else:
        #     is_token_kind(scanner.next_token, T_COMMA, T_RPAREN)

    return parse_tree


def statement(scanner):
    parse_tree = ParseTree(N_STATEMENT, scanner.get_line_number())

    token = scanner.next_token
    if token.kind == T_LCURLY:
        parse_tree.add(compound_stmt(scanner))
    elif token.kind == T_IF:
        parse_tree.add(if_stmt(scanner))
    elif token.kind == T_WHILE:
        parse_tree.add(while_stmt(scanner))
    elif token.kind == T_RETURN:
        parse_tree.add(return_stmt(scanner))
    elif token.kind == T_WRITE or token.kind == T_WRITELN:
        parse_tree.add(write_stmt(scanner))
    else:
        parse_tree.add(expression_stmt(scanner))
    return parse_tree


def expression_stmt(scanner):
    parse_tree = ParseTree(N_EXPRESSION_STMT, scanner.get_line_number())

    if scanner.next_token.kind == T_SEMICOL:
        parse_tree.add(scanner.next_token)
    else:
        # N_EXPRESSION
        parse_tree.add(expression(scanner))

        # T_SEMICOL
        parse_tree.add(
            is_token_kind(scanner.next_token, T_SEMICOL)
            )

    scanner.get_next_token()

    return parse_tree


def expression(scanner):
    parse_tree = ParseTree(N_EXPRESSION, scanner.get_line_number())

    scanner.set_backtrack_index()
    # N_VAR
    parse_tree_var = var(scanner, parse_error=False)
    # T_ASSIGN
    parse_tree_assign = expression_assign(scanner, parse_error=False)

    if parse_tree_var and parse_tree_assign:
        parse_tree.children.extend([parse_tree_var, parse_tree_assign])
        # N_EXPRESSION
        parse_tree.add(expression(scanner))
        scanner.unset_backtrack_index()
    else:
        scanner.backtrack()
        # N_EXPRESSION
        parse_tree.add(
            comp_exp(scanner)
            )

    return parse_tree


def expression_assign(scanner, parse_error=True):
    try:
        # T_ASSIGN
        assign = is_token_kind(
            scanner.next_token, T_ASSIGN, parse_error=parse_error
            )
        scanner.get_next_token()
        return assign
    except BackTrackError:
        return None


def var(scanner, parse_error=True):
    try:
        parse_tree = ParseTree(N_VAR, scanner.get_line_number())

        if scanner.next_token.kind == T_MUL:
            # T_MUL
            parse_tree.add(
                is_token_kind(
                    scanner.next_token, T_MUL, parse_error=parse_error
                    )
                )
            scanner.get_next_token()

        # T_ID
        parse_tree.add(
            is_token_kind(
                scanner.next_token, T_ID, parse_error=parse_error
                )
            )
        scanner.get_next_token()

        # T_LBRACK N_EXPRESSION T_RBRACK
        if scanner.next_token.kind == T_LBRACK:
            # T_LBRACK
            parse_tree.add(
                is_token_kind(
                    scanner.next_token, T_LBRACK, parse_error=parse_error
                    )
                )
            scanner.get_next_token()
            # N_EXPRESSION
            parse_tree.add(
                expression(scanner)
                )
            # T_RBRACK
            parse_tree.add(
                is_token_kind(
                    scanner.next_token, T_RBRACK, parse_error=parse_error
                    )
                )
            scanner.get_next_token()
        return parse_tree
    except BackTrackError:
        return None


def comp_exp(scanner):
    parse_tree = ParseTree(N_COMP_EXP, scanner.get_line_number())

    # N_E
    parse_tree.add(e(scanner))
    if _is_relop(scanner.next_token):
        # N_RELOP
        parse_tree.add(relop(scanner))
        # N_E
        parse_tree.add(e(scanner))

    return parse_tree


def _is_relop(token):
    is_relop_tokens = [T_LEQ, T_LES, T_EQU, T_NEQ, T_GRE, T_GEQ]
    return token.kind in is_relop_tokens


def relop(scanner):
    parse_tree = ParseTree(N_RELOP, scanner.get_line_number())

    # T_LEQ, T_LES, T_EQU, T_NEQ, T_GRE, T_GEQ
    parse_tree.add(
        is_token_kind(
            scanner.next_token,
            T_LEQ, T_LES, T_EQU, T_NEQ, T_GRE, T_GEQ
            )
        )
    scanner.get_next_token()

    return parse_tree


def e(scanner):
    parse_tree = ParseTree(N_E, scanner.get_line_number())

    # N_T
    parse_tree.add(t(scanner))
    while _is_addop(scanner.next_token):
        parse_tree_top = ParseTree(N_E, parse_tree.line_number)
        parse_tree_top.children.append(parse_tree)
        parse_tree = parse_tree_top
        # N_ADDOP
        parse_tree.add(addop(scanner))
        # N_T
        parse_tree.add(t(scanner))

    return parse_tree


def _is_addop(token):
    is_addop_tokens = [T_PLU, T_MIN]
    return token.kind in is_addop_tokens


def addop(scanner):
    parse_tree = ParseTree(N_ADDOP, scanner.get_line_number())

    # T_PLU, T_MIN
    parse_tree.add(
        is_token_kind(
            scanner.next_token,
            T_PLU, T_MIN
            )
        )
    scanner.get_next_token()

    return parse_tree


def t(scanner):
    parse_tree = ParseTree(N_T, scanner.get_line_number())

    # N_F
    parse_tree.add(f(scanner))
    while _is_mulop(scanner.next_token):
        parse_tree_top = ParseTree(N_T, parse_tree.line_number)
        parse_tree_top.children.append(parse_tree)
        parse_tree = parse_tree_top
        # N_MULOP
        parse_tree.add(mulop(scanner))
        # N_F
        parse_tree.add(f(scanner))

    return parse_tree


def _is_mulop(token):
    is_mulop_tokens = [T_MUL, T_DIV, T_MOD]
    return token.kind in is_mulop_tokens


def mulop(scanner):
    parse_tree = ParseTree(N_MULOP, scanner.get_line_number())

    # T_MUL, T_DIV, T_MOD
    parse_tree.add(
        is_token_kind(
            scanner.next_token,
            T_MUL, T_DIV, T_MOD
            )
        )
    scanner.get_next_token()

    return parse_tree


def f(scanner):
    parse_tree = ParseTree(N_F, scanner.get_line_number())

    if scanner.next_token.kind in [T_MIN, T_AND, T_MUL]:
        # T_MIN, T_AND, T_MUL
        parse_tree.add(
            is_token_kind(scanner.next_token, T_MIN, T_AND, T_MUL)
            )
        scanner.get_next_token()

    parse_tree.add(factor(scanner))

    return parse_tree


def factor(scanner):
    parse_tree = ParseTree(N_FACTOR, scanner.get_line_number())

    if scanner.next_token.kind == T_LPAREN:
        # T_LPAREN
        parse_tree.add(
            is_token_kind(scanner.next_token, T_LPAREN)
            )
        scanner.get_next_token()
        # N_EXPRESSION
        parse_tree.add(expression(scanner))
        # T_RPAREN
        parse_tree.add(
            is_token_kind(scanner.next_token, T_RPAREN)
            )
        scanner.get_next_token()
    elif scanner.next_token.kind == T_READ:
        # T_READ
        parse_tree.add(
            is_token_kind(scanner.next_token, T_READ)
            )
        scanner.get_next_token()
        # T_LPAREN
        parse_tree.add(
            is_token_kind(scanner.next_token, T_LPAREN)
            )
        scanner.get_next_token()
        # T_RPAREN
        parse_tree.add(
            is_token_kind(scanner.next_token, T_RPAREN)
            )
        scanner.get_next_token()
    elif scanner.next_token.kind in [T_NUM, T_STRLIT]:
        # T_NUM, T_STRLIT
        parse_tree.add(
            is_token_kind(scanner.next_token, T_NUM, T_STRLIT)
            )
        scanner.get_next_token()
    else:
        scanner.set_backtrack_index()

        id1 = is_token_kind(scanner.next_token, T_ID)
        scanner.get_next_token()

        if scanner.next_token.kind == T_LBRACK:
            # T_ID
            parse_tree.add(id1)
            # T_LBRACK
            parse_tree.add(
                is_token_kind(scanner.next_token, T_LBRACK)
                )
            scanner.get_next_token()
            # N_EXPRESSION
            parse_tree.add(expression(scanner))
            # T_RBRACK
            parse_tree.add(
                is_token_kind(scanner.next_token, T_RBRACK)
                )
            scanner.get_next_token()
            scanner.unset_backtrack_index()
        elif scanner.next_token.kind == T_LPAREN:
            scanner.backtrack()
            parse_tree.add(fun_call(scanner))
        else:
            scanner.backtrack()
            # T_ID
            parse_tree.add(
                is_token_kind(scanner.next_token, T_ID)
                )
            scanner.get_next_token()

    return parse_tree


def fun_call(scanner):
    parse_tree = ParseTree(N_FUN_CALL, scanner.get_line_number())

    # T_ID
    parse_tree.add(
        is_token_kind(scanner.next_token, T_ID)
        )
    scanner.get_next_token()
    # T_LPAREN
    parse_tree.add(is_token_kind(scanner.next_token, T_LPAREN))
    scanner.get_next_token()
    # N_ARGS
    parse_tree.add(args(scanner))
    # T_RPAREN
    parse_tree.add(is_token_kind(scanner.next_token, T_RPAREN))
    scanner.get_next_token()

    return parse_tree


def args(scanner):
    parse_tree = ParseTree(N_ARGS, scanner.get_line_number())

    # N_ARG_LIST
    if not _is_end_of_arg_list(scanner.next_token):
        parse_tree.add(arg_list(scanner))

    return parse_tree


def _is_end_of_arg_list(token):
    end_of_arg_list_tokens = [T_RPAREN]
    return token.kind in end_of_arg_list_tokens


def arg_list(scanner):
    parse_tree = ParseTree(N_ARG_LIST, scanner.get_line_number())

    # N_EXPRESSION (minimum 1 expression required)
    parse_tree.add(expression(scanner))
    while not _is_end_of_arg_list(scanner.next_token):
        parse_tree_top = ParseTree(N_ARG_LIST, parse_tree.line_number)
        parse_tree_top.children.append(parse_tree)
        parse_tree = parse_tree_top
        parse_tree.add(is_token_kind(scanner.next_token, T_COMMA))
        scanner.get_next_token()
        parse_tree.add(expression(scanner))

    return parse_tree


def compound_stmt(scanner):
    parse_tree = ParseTree(N_COMPOUND_STMT, scanner.get_line_number())

    # T_LCURLY
    parse_tree.add(is_token_kind(scanner.next_token, T_LCURLY))
    scanner.get_next_token()
    # N_LOCAL_DECS
    parse_tree.add(local_decs(scanner))
    # N_STATEMENT_LIST
    parse_tree.add(statement_list(scanner))
    # T_RCURLY
    parse_tree.add(is_token_kind(scanner.next_token, T_RCURLY))
    scanner.get_next_token()

    return parse_tree


def local_decs(scanner):
    parse_tree = ParseTree(N_LOCAL_DECS, scanner.get_line_number())
    while not _is_end_of_local_decs(scanner.next_token):
        parse_tree_top = ParseTree(N_LOCAL_DECS, parse_tree.line_number)
        parse_tree_top.children.append(parse_tree)
        parse_tree = parse_tree_top
        parse_tree.add(var_dec(scanner))

    return parse_tree


def _is_end_of_local_decs(token):
    end_of_local_decs_tokens = [T_INT, T_VOID, T_STRING]
    return token.kind not in end_of_local_decs_tokens


def statement_list(scanner):
    parse_tree = ParseTree(N_STATEMENT_LIST, scanner.get_line_number())
    while not _is_end_of_statement_list(scanner.next_token):
        parse_tree_top = ParseTree(N_STATEMENT_LIST, parse_tree.line_number)
        parse_tree_top.children.append(parse_tree)
        parse_tree = parse_tree_top
        parse_tree.add(statement(scanner))

    return parse_tree


def _is_end_of_statement_list(token):
    end_of_statement_list_tokens = [T_RCURLY]
    return token.kind in end_of_statement_list_tokens


def while_stmt(scanner):
    parse_tree = ParseTree(N_WHILE_STMT, scanner.get_line_number())

    # T_WHILE
    parse_tree.add(is_token_kind(scanner.next_token, T_WHILE))
    scanner.get_next_token()
    # T_LPAREN
    parse_tree.add(is_token_kind(scanner.next_token, T_LPAREN))
    scanner.get_next_token()
    # N_EXPRESSION
    parse_tree.add(expression(scanner))
    # T_RPAREN
    parse_tree.add(is_token_kind(scanner.next_token, T_RPAREN))
    scanner.get_next_token()
    # N_STATEMENT
    parse_tree.add(statement(scanner))
    # scanner.get_next_token()

    return parse_tree


def if_stmt(scanner):
    parse_tree = ParseTree(N_IF_STMT, scanner.get_line_number())

    # T_IF
    parse_tree.add(is_token_kind(scanner.next_token, T_IF))
    scanner.get_next_token()
    # T_LPAREN
    parse_tree.add(is_token_kind(scanner.next_token, T_LPAREN))
    scanner.get_next_token()
    # N_EXPRESSION
    parse_tree.add(expression(scanner))
    # T_RPAREN
    parse_tree.add(is_token_kind(scanner.next_token, T_RPAREN))
    scanner.get_next_token()
    # N_STATEMENT
    parse_tree.add(statement(scanner))
    # scanner.get_next_token()

    # T_ELSE
    if scanner.next_token.kind == T_ELSE:
        parse_tree.add(scanner.next_token)
        scanner.get_next_token()
        # N_STATEMENT
        parse_tree.add(statement(scanner))

    return parse_tree


def return_stmt(scanner):
    parse_tree = ParseTree(N_RETURN_STMT, scanner.get_line_number())

    # T_RETURN
    parse_tree.add(is_token_kind(scanner.next_token, T_RETURN))
    scanner.get_next_token()

    if scanner.next_token.kind == T_SEMICOL:
        # T_SEMICOL
        parse_tree.add(
            is_token_kind(scanner.next_token, T_SEMICOL)
            )
    else:
        # N_EXPRESSION
        parse_tree.add(expression(scanner))
        # T_SEMICOL
        parse_tree.add(
            is_token_kind(scanner.next_token, T_SEMICOL)
            )

    scanner.get_next_token()

    return parse_tree


def write_stmt(scanner):
    parse_tree = ParseTree(N_WRITE_STMT, scanner.get_line_number())

    if scanner.next_token.kind == T_WRITE:
        # T_WRITE
        parse_tree.add(is_token_kind(scanner.next_token, T_WRITE))
        scanner.get_next_token()
        # T_LPAREN
        parse_tree.add(is_token_kind(scanner.next_token, T_LPAREN))
        scanner.get_next_token()
        # N_EXPRESSION
        parse_tree.add(expression(scanner))
        # T_RPAREN
        parse_tree.add(is_token_kind(scanner.next_token, T_RPAREN))
        scanner.get_next_token()
        # T_SEMICOL
        parse_tree.add(
            is_token_kind(scanner.next_token, T_SEMICOL)
            )
        scanner.get_next_token()

    else:
        # T_WRITELN
        parse_tree.add(
            is_token_kind(scanner.next_token, T_WRITELN)
            )
        scanner.get_next_token()
        # T_LPAREN
        parse_tree.add(is_token_kind(scanner.next_token, T_LPAREN))
        scanner.get_next_token()
        # T_RPAREN
        parse_tree.add(is_token_kind(scanner.next_token, T_RPAREN))
        scanner.get_next_token()
        # T_SEMICOL
        parse_tree.add(
            is_token_kind(scanner.next_token, T_SEMICOL)
            )
        scanner.get_next_token()

    return parse_tree


def is_token_kind(token, *token_kind, parse_error=True):
    if token.kind in token_kind:
        return token
    elif parse_error:
        raise ParseError(token.value, token.line_number)
    else:
        raise BackTrackError


class MuddParser():
    """Recursive Descent Parser.

    """
    def __init__(self, filename):
        self.scanner = MuddScanner(filename)
        self.parse_tree = None

    def parse(self):
        self.scanner.get_next_token()
        self.parse_tree = program(self.scanner)
        if self.scanner.next_token.kind == T_EOF:
            return self.parse_tree
        else:
            raise ParseError(
                self.scanner.next_token.value,
                self.scanner.next_token.line_number
                )


class ParseError(Exception):
    def __init__(self, value, line_number):
        self.value = value
        self.line_number = line_number

    def __str__(self):
        return '[ParseError] Error parsing value \'%s\' at line %d' % (
            self.value, self.line_number
            )


class BackTrackError(Exception):
    pass
