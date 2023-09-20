from cmdu.lines import LineNumberAppender


def cmd_set_nu(ins, out):
    appender = LineNumberAppender()
    for l in ins:
        out.write(appender.append(l))
