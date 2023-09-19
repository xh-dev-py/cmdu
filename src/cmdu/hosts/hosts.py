import re


class HostItem:
    def __init__(self, ip: str, hosts: [str], padding):
        self.ip = ip
        self.hosts = hosts
        self.padding = padding

    def add_hostname(self, name):
        if name in self.hosts:
            return self
        self.hosts.append(name)
        return self

    def remove_hostname(self, name):
        if name in self.hosts:
            self.hosts.remove(name)
        return self

    def valid(self):
        return len(self.hosts) > 0

    @staticmethod
    def from_line(line):
        if line == "\n":
            return None

        if line.endswith("\n"):
            line = line[:-1]

        reg = re.compile("^([0-9:.]+)( +)(.*)$")
        matching = reg.search(line)
        if not matching:
            return None
        ip = matching.group(1)
        padding = matching.group(2)
        hosts = matching.group(3).split(" ")
        return HostItem(ip, hosts, padding)

    def __str__(self):
        self.to_line()

    def __repr__(self):
        return self.__str__()

    def to_line(self):
        if not self.valid():
            return None
        elif len(self.hosts) == 1:
            hosts = " ".join(self.hosts)
            return f"{self.ip}{self.padding}{hosts}"
        else:
            hosts = " ".join(self.hosts)
            return f"{self.ip}{self.padding}{hosts[1:]}"


class Hosts:
    def __init__(self, hosts: [HostItem]):
        self._hosts = hosts

