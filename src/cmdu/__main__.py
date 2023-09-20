import argparse
import re
import sys

from cmdu import load_json, load_yaml, as_json, as_yaml
from cmdu.check_list import CheckListItem
from cmdu.hosts import HostItem
from cmdu.lines import LineNumberAppender


def json2yaml(data: str):
    return as_yaml(load_json(data))


def yaml2json(data: str, indent=None):
    return as_json(load_yaml(data), indent)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='cmdu',
    )
    parser.add_argument("--from-file", default=None)

    sparser = parser.add_subparsers(dest="command")

    file_mod_parser = sparser.add_parser("file-mod", help="modify file")
    file_mod_sub_parser = file_mod_parser.add_subparsers(dest="sub_command")
    file_mod_sub_hosts_parser = file_mod_sub_parser.add_parser("hosts", help="modify hosts file")
    file_mod_sub_hosts_sub_parser = file_mod_sub_hosts_parser.add_subparsers(dest="sub_sub_command")
    file_mod_sub_hosts_sub_mod_parser = file_mod_sub_hosts_sub_parser.add_parser("mod", help="add hosts")
    file_mod_sub_hosts_sub_mod_parser.add_argument("-i", "--ip", required=True, help="ip address")
    file_mod_sub_hosts_sub_mod_action_parser = file_mod_sub_hosts_sub_mod_parser.add_mutually_exclusive_group()
    file_mod_sub_hosts_sub_mod_action_parser.add_argument("-a", "--add", action='store_true', default=False,
                                                          help="add a host")
    file_mod_sub_hosts_sub_mod_action_parser.add_argument("-d", "--delete", action='store_true', default=False,
                                                          help="delete a host")
    file_mod_sub_hosts_sub_mod_action_parser.add_argument("--delete-all", action='store_true', default=False,
                                                          help="delete all hosts")
    file_mod_sub_hosts_sub_mod_parser.add_argument("--host", required=False, help="host name")

    check_list_parser = sparser.add_parser("check-list", help="make check list for lines")
    check_list_s_parser = check_list_parser.add_subparsers(dest="sub_command")
    check_list_s_parser.add_parser("create", help="make check list by list of lines input")
    check_list_s_load_parser = check_list_s_parser.add_parser("load", help="make check list by list of lines input")
    check_list_s_load_g_input_parser = check_list_s_load_parser.add_mutually_exclusive_group()
    check_list_s_load_g_input_parser.add_argument("--yaml-in", action='store_true', default=False)
    check_list_s_load_g_input_parser.add_argument("--json-in", action='store_true', default=False)
    check_list_s_load_g_input_parser.add_argument("--simple-in", action='store_true', default=False)
    check_list_s_load_g_output_parser = check_list_s_load_parser.add_mutually_exclusive_group()
    check_list_s_load_g_output_parser.add_argument("--yaml-out", action='store_true', default=False)
    check_list_s_load_g_output_parser.add_argument("--json-out", action='store_true', default=False)
    check_list_s_load_g_output_parser.add_argument("--simple-out", action='store_true', default=False)
    check_list_s_load_parser.add_argument("-l", "--lean", action='store_true', default=False,
                                          help="remove unnecessary empty line[simple-out only]")
    check_list_s_load_parser.add_argument("-p", "--pretty", action='store_true', default=False,
                                          help="prettify the json string [json-out only]")
    check_list_s_load_parser.add_argument("--indent", default=4)

    check_list_s_parser.add_parser("check", help="check list by list of lines input") \
        .add_argument("indexes", type=int, nargs="+", help="indexes of lines to be checked")
    check_list_s_parser.add_parser("uncheck", help="uncheck list by list of lines input") \
        .add_argument("indexes", type=int, nargs="+", help="indexes of lines to be unchecked")

    line_s_parser = sparser.add_parser("lines")
    line_s_s_parser = line_s_parser.add_subparsers(dest="sub_command")
    line_numberParser = line_s_s_parser.add_parser("set-nu", help="pad line number to each line")

    line_s_s_parser.add_parser("count", help="calculate number of lines")
    lines_trim_parser = line_s_s_parser.add_parser("trim", help="trim lines by delimiter")
    lines_trim_parser.add_argument("-c", "--character", required=True, help="character to trim")
    lines_trim_action_parser = lines_trim_parser.add_mutually_exclusive_group()
    lines_trim_action_parser.add_argument("-l", "--left", action='store_true', default=False, help="trim left")
    lines_trim_action_parser.add_argument("-r", "--right", action='store_true', default=False, help="trim right")
    lines_trim_action_parser.add_argument("-a", "--all", action='store_true', default=False,
                                          help="trim both left and right")

    lines_split_parser = line_s_s_parser.add_parser("split", help="split lines by delimiter")
    lines_split_parser.add_argument("-d", "--delimiter", required=True, help="delimiter")

    lines_skip_parser = line_s_s_parser.add_parser("skip", help="skip number of lines")
    lines_skip_parser.add_argument("-n", "--number", default=0)
    lines_filter_parser = line_s_s_parser.add_parser("filter", help="filter lines by regex [*experimental]")
    lines_filter_parser.add_argument("-r", "--regex", default=None)

    lines_filter_not_parser = line_s_s_parser.add_parser("filter-not",
                                                         help="filter not match lines by regex [*experimental]")
    lines_filter_not_parser.add_argument("-r", "--regex", default=None)

    convert_parser = sparser.add_parser("convert")
    convert_sub_parser = convert_parser.add_subparsers(dest="sub_command")
    json2yamlParser = convert_sub_parser.add_parser("j2y", help="Convert json to yaml")
    yaml2jsonParser = convert_sub_parser.add_parser("y2j", help="Convert yaml to json")
    yaml2jsonParser.add_argument("-p", "--pretty", action=argparse.BooleanOptionalAction, default=False)
    yaml2jsonParser.add_argument("--indent", default=4)
    asJsonParser = convert_sub_parser.add_parser("j2j", help="Convert json string to json of specific format")
    asJsonParser.add_argument("-p", "--pretty", action=argparse.BooleanOptionalAction, default=False)
    asJsonParser.add_argument("--indent", default=4)

    args = parser.parse_args()

    ins = sys.stdin
    out = sys.stdout
    sys.stdout = sys.stderr

    if args.from_file is not None:
        f = open(args.from_file)
        ins = f

    if args.command == "file-mod":
        if args.sub_command == "hosts":
            if args.sub_sub_command == "mod":
                if args.add:
                    if args.host is None:
                        raise Exception("host name is required")

                    found = False
                    for l in ins:
                        item = HostItem.from_line(l)
                        if item is not None and item.ip == args.ip:
                            found = True
                            item.add_hostname(args.host)
                            out.write(item.to_line())
                            out.write("\n")
                        else:
                            if l.endswith("\n"):
                                out.write(l)
                            else:
                                out.write(l)
                                out.write("\n")

                    if not found:
                        out.write(HostItem(args.ip, [args.host], "          ").to_line())
                        out.write("\n")
                elif args.delete:
                    for l in ins:
                        if args.host is None:
                            raise Exception("host name is required")
                        item = HostItem.from_line(l)
                        if item is not None and item.ip == args.ip:
                            item.remove_hostname(args.host)
                            if item.valid():
                                out.write(item.to_line())
                                out.write("\n")
                        else:
                            out.write(l)
                elif args.delete_all:
                    for l in ins:
                        item = HostItem.from_line(l)
                        if item is not None and item.ip == args.ip:
                            continue
                        else:
                            out.write(l)
                else:
                    raise Exception("Not support")
            else:
                raise Exception("not implemented")
        else:
            raise Exception("not implemented")
    elif args.command == "check-list":
        if args.sub_command == "create":
            appender = LineNumberAppender()
            for l in ins:
                if l == "\n":
                    out.write(l)
                    continue
                line = appender.append(l)
                out.write(f"[ ] {line}")
        elif args.sub_command == "load":
            in_data = []
            if args.simple_in:
                in_data = [CheckListItem.from_line(x) for x in ins.readlines() if x != ""]
            elif args.yaml_in:
                m = load_yaml(ins.read())
                in_data = [CheckListItem.from_dict(m[k]) for k in m]
            elif args.json_in:
                m = load_json(ins.read())
                in_data = [CheckListItem.from_dict(m[k]) for k in m]

            if args.simple_out:
                for l in in_data:
                    if l is None:
                        if args.lean:
                            continue
                        out.write("\n")
                    else:
                        out.write(l.to_line())
            elif args.yaml_out:
                yaml_str = as_yaml([x.to_dict() for x in in_data if x is not None])
                out.write(yaml_str)
            elif args.json_out:
                json_str = as_json([x.to_dict() for x in in_data if x is not None],
                                   args.indent if args.pretty else int(args.indent))
                out.write(json_str)
        elif args.sub_command == "uncheck":
            indexes = args.indexes
            appender = LineNumberAppender()
            id_reg = re.compile("^\\[[Xx]] (\\d{6}) \\|")
            for l in ins:
                if l == "\n":
                    out.write(l)
                    continue
                matching = id_reg.search(l)
                if not matching:
                    out.write(l)
                    continue

                id = int(matching.group(1))
                if id in indexes:
                    line = appender.append(l[12:])
                    out.write(f"[ ] {line}")
                else:
                    out.write(l)
        elif args.sub_command == "check":
            indexes = args.indexes
            appender = LineNumberAppender()
            id_reg = re.compile("^\\[ ] (\\d{6}) \\|")
            for l in ins:
                if l == "\n":
                    out.write(l)
                    continue
                matching = id_reg.search(l)
                if not matching:
                    out.write(l)
                    continue

                id = int(matching.group(1))
                if id in indexes:
                    line = appender.append(l[12:])
                    out.write(f"[x] {line}")
                else:
                    out.write(l)
    elif args.command == "lines":
        cmd = args.command
        if args.sub_command == "set-nu":
            appender = LineNumberAppender()
            for l in ins:
                out.write(appender.append(l))
        elif args.sub_command == "split":
            for l in ins:
                ls = l.rstrip("\n").split(args.delimiter)
                for x in ls:
                    out.write(x)
                    out.write("\n")

        elif args.sub_command == "count":
            count = 0
            for l in ins:
                count += 1
            out.write(f"{count}")
        elif args.sub_command == "trim":
            for l in ins:
                l = l.rstrip("\n")
                if args.left:
                    l = l.lstrip(args.character)
                if args.right:
                    l = l.rstrip(args.character)
                if args.all:
                    l = l.strip(args.character)
                out.write(l)
                out.write("\n")
        elif args.sub_command == "skip":
            count = 0
            to_be_skipped = int(args.number)
            for l in ins:
                count += 1
                if count > to_be_skipped:
                    out.write(l)
        elif args.sub_command == "filter":
            regex = re.compile(args.regex)
            for l in ins:
                if regex.search(l):
                    out.write(l)
        elif args.sub_command == "filter-not":
            regex = re.compile(args.regex)
            for l in ins:
                if not regex.search(l):
                    out.write(l)
        else:
            raise Exception("Sub command not support")
    elif args.command == "convert":
        if args.sub_command == "j2y":
            data = "\n".join(ins.readlines())
            out.write(json2yaml(data))
        elif args.sub_command == "y2j":
            data = "\n".join(ins.readlines())
            out.write(yaml2json(data, int(args.indent) if args.pretty else None))
        elif args.sub_command == "j2j":
            data = "\n".join(ins.readlines())
            out.write(as_json(load_json(data), int(args.indent) if args.pretty else None))
        else:
            raise Exception("Sub command not support")
    else:
        raise Exception("Command not support")
    out.write("\n")
