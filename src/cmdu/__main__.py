import argparse
import sys

from cmdu import load_json, load_yaml, as_json, as_yaml
from cmdu.lines import LineNumberAppender


def json2yaml(data: str):
    return as_yaml(load_json(data))


def yaml2json(data: str, indent=None):
    return as_json(load_yaml(data), indent)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='cmdu',
    )
    sparser = parser.add_subparsers(dest="command")
    parser.add_argument("--from-file", default=None)
    line_numberParser = sparser.add_parser("set-ln", help="pad line number to each line")

    json2yamlParser = sparser.add_parser("json2yaml", help="Convert json to yaml")
    yaml2jsonParser = sparser.add_parser("yaml2json", help="Convert yaml to json")
    yaml2jsonParser.add_argument("-p", "--pretty", action=argparse.BooleanOptionalAction, default=False)
    yaml2jsonParser.add_argument("--indent", default=4)
    asJsonParser = sparser.add_parser("json2json", help="Convert json string to json of specific format")
    asJsonParser.add_argument("-p", "--pretty", action=argparse.BooleanOptionalAction, default=False)

    args = parser.parse_args()

    if args.from_file is not None:
        f = open(args.from_file)
        sys.stdin = f

    if args.command == "set-ln":
        appender = LineNumberAppender()
        for l in sys.stdin:
            sys.stdout.write(appender(l))
    elif args.command == "json2yaml":
        data = "\n".join(sys.stdin.readlines())
        sys.stdout.write(json2yaml(data))
    elif args.command == "yaml2json":
        data = "\n".join(sys.stdin.readlines())
        sys.stdout.write(yaml2json(data, int(args.indent) if args.pretty else None))
    elif args.command == "json2json":
        data = "\n".join(sys.stdin.readlines())
        sys.stdout.write(as_json(load_json(data), int(args.indent) if args.pretty else None))
