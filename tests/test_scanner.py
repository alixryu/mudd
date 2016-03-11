from mudd import T_INT, T_ID, T_EOF, KIND_NAME
from mudd.scanner import Token, MuddScanner as Scanner


def test_token():
    check_token_constructor()


def check_token_constructor():
    id_token = Token(T_ID, 1, 'num')
    int_token = Token(T_INT, 2, 'int')
    assert id_token is not None
    assert int_token is not None
    check_token_repr(id_token, T_ID, 1, 'num')
    check_token_repr(int_token, T_INT, 2, 'int')


def check_token_repr(token, kind, line_number, value):
    expected = 'Token: %s\tValue: %s\t\tLine: %s\n' % (
        str(KIND_NAME[kind]), str(value), str(line_number)
        )
    assert str(token) == expected


def test_scanner():
    scanner = Scanner('factorial.bpl')
    check_scanner_get_next_token(scanner)


def check_scanner_get_next_token(scanner):
    trigger = True
    while trigger:
        scanner.get_next_token()
        token = scanner.next_token
        print(token)
        if token.kind == T_EOF:
            trigger = False
    assert True
