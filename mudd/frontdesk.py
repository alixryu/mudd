import sys

from mudd.parser import MuddParser, ParseError


if __name__ == '__main__':
    try:
        parser = MuddParser(sys.argv[1])
        parser.parse()
        print(parser.parse_tree)

    except IndexError:
        print('[IndexError] No compilable file received as argument.')

    except FileNotFoundError:
        print('[FileNotFoundError] No such file is found.')

    except SyntaxError:
        print('[SyntaxError] Unclosed comment exists.')

    except ParseError as parse_error:
        print(parse_error)
