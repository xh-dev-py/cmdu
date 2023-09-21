from cmdu.lines import LineNumberAppender


def cmd_set_nu(ins, out):
    appender = LineNumberAppender()
    for l in ins:
        out.write(appender.append(l))


def cmd_set_split(ins, out, delimiter):
    for l in ins:
        ls = l.rstrip("\n").split(delimiter)
        for x in ls:
            out.write(f"{x}\n")
