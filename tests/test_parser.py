from mudd import T_EOF
from mudd.parser import MuddParser


def test_parse_constructor():
    assert 'parse' in MuddParser.__dict__.keys()
    parser = MuddParser('factorial.bpl')
    test_parser_attributes = parser.__dict__.keys()
    assert 'scanner' in test_parser_attributes
    assert 'parse_tree' in test_parser_attributes


def test_parse():
    parser = MuddParser('factorial.bpl')
    # test reaching reject
    assert parser.parse() is None

    # test reaching accept by EOF
    scanner = parser.scanner
    trigger = True
    while trigger:
        scanner.get_next_token()
        token = scanner.next_token
        if token.kind == T_EOF:
            trigger = False

    assert parser.parse() is None
