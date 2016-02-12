from scanner import Token, MuddScanner as Scanner
from scanner import T_INT, T_ID, T_EOF


def test_token():
    test_token_constructor()


def test_token_constructor():
    id_token = Token(T_ID, 1, 'num')
    int_token = Token(T_INT, 2, 'int')
    assert id_token is not None
    assert int_token is not None
    test_token_repr(id_token, T_ID, 1, 'num')
    test_token_repr(int_token, T_INT, 2, 'int')


def test_token_repr(token, kind, line_number, value):
    expected = 'Kind: %s\tValue: %s\t\tLine: %s' % (
        str(kind), str(value), str(line_number)
        )
    assert str(token) == expected


def test_scanner():
    scanner = Scanner('factorial.bpl')
    test_scanner_get_next_token(scanner)


def test_scanner_get_next_token(scanner):
    trigger = True
    while trigger:
        scanner.get_next_token()
        token = scanner.next_token
        print(token)
        if token.kind == T_EOF:
            trigger = False
    assert True


if __name__ == '__main__':
    test_token()
    test_scanner()
