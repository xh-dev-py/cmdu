from unittest import TestCase

from cmdu.lines.cmd_set_nu import cmd_set_nu, cmd_set_split


class Writer:
    def __init__(self):
        self.lines = []

    def write(self, line):
        self.lines.append(line)


class TestLine(TestCase):
    def test_set_nu(self):
        writer = Writer()
        test_input = ["a", "b", "c"]
        cmd_set_nu(test_input, writer)
        write = writer.lines
        self.assertEqual(len(write), 3)
        self.assertEqual(write[0], "000001 |a")
        self.assertEqual(write[1], "000002 |b")
        self.assertEqual(write[2], "000003 |c")

    def test_split(self):
        writer = Writer()
        test_input = ["a|x", "bx", "c|x"]
        cmd_set_split(test_input, writer, "|")
        write = writer.lines
        self.assertEqual(len(write), 5)
        self.assertEqual(write[0], "a\n")
        self.assertEqual(write[1], "x\n")
        self.assertEqual(write[2], "bx\n")
        self.assertEqual(write[3], "c\n")
        self.assertEqual(write[4], "x\n")
