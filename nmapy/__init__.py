from nmapy import parser

def parse(args):
    nmapy_parser = parser.Parser(args.file)
    nmapy_parser.delimiter = args.delimiter
    if args.display not in nmapy_parser.display_functions.keys():
        print('\nInvalid display option, vaid options:')
        for function in nmapy_parser.display_functions.keys():
            print(f' - {function}')
        print()
        return
    nmapy_parser.display_functions[args.display]()
