from .scanner import MuddScanner

from mudd import *


class MuddParser():
    """Recursive Descent Parser.

    """
    def __init__(self, filename):
        self.scanner = MuddScanner(filename)
        self.parse_tree = None

    def parse(self):
        self.scanner.get_next_token()
        tree_node = None  # Program()
        if self.scanner.next_token.kind == T_EOF:
            print('Accept')
            return tree_node
        else:
            print('Reject')
            return None
