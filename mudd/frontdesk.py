import sys

from mudd.parser import ParseError
from mudd.typechecker import MuddTypeChecker, TypeCheckError


if __name__ == '__main__':
    try:
        args = sys.argv
        debug = False

        if len(args) <= 1:
            sys.exit(0)

        if '--debug' in args:
            debug = True

        type_checker = MuddTypeChecker(args[-1], debug)

        if '--tree' in args:
            print(type_checker.parse_tree)

        type_checker.top_down_pass()
        type_checker.bottom_up_pass()


    except IndexError:
        print('[IndexError] No compilable file received as argument.')

    except FileNotFoundError:
        print('[FileNotFoundError] No such file is found.')

    except SyntaxError as syntax_error:
        print('[SyntaxError] %s' % syntax_error)

    except ParseError as parse_error:
        print(parse_error)

    except TypeCheckError as type_check_error:
        print(type_check_error)
