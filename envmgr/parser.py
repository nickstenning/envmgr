from collections import defaultdict
import os
import logging
import re
import string

log = logging.getLogger(__name__)


class ParseError(Exception):
    pass


class EnvConfParser(object):

    def __init__(self, name, root, start=None):
        self.name = name
        self.root = root

        if start is None:
            self.env = os.environ.copy()
        else:
            self.env = start.copy()

    def parse(self):
        fname = self._get_fname()

        try:
            fp = open(fname)
        except IOError:
            log.warn("Couldn't open envmgr config '%s': treating as blank!", fname)
        else:
            with fp:
                for line in fp:
                    self.parse_line(line)

        return self.env

    def parse_line(self, line):
        line = line.strip()

        # Skip blank lines
        if not line:
            return

        # Skip comment lines
        if line.startswith('#'):
            return

        if line.startswith('include '):
            self.include(line[8:])
        elif line.startswith('unset '):
            self.unset(line[6:])
        elif line == 'clear':
            self.clear()
        else:
            self.parse_env_line(line)

    def include(self, line):
        name = line.strip()
        parser = EnvConfParser(name, self.root, self.env)
        self.env = parser.parse()

    def unset(self, line):
        var = line.strip()
        if var in self.env:
            del self.env[var]

    def clear(self):
        self.env = {}

    def parse_env_line(self, line):
        interpolate = True
        line = line.strip()
        m1 = re.match(r'\A([A-Za-z_][A-Za-z_0-9]*)=(.*)\Z', line)
        if m1:
            key, val = m1.group(1), m1.group(2)

            m2 = re.match(r"\A'(.*)'\Z", val)
            if m2:
                interpolate = False
                val = m2.group(1)

            m3 = re.match(r'\A"(.*)"\Z', val)
            if m3:
                val = re.sub(r'\\(.)', r'\1', m3.group(1))

            if interpolate:
                env_default_blank = defaultdict(str)
                env_default_blank.update(self.env)

                val = string.Template(val).substitute(env_default_blank)

            self.env[key] = val
        else:
            raise ParseError("Could not parse line: '%s' (%s)" % (line, self.name))

    def _get_fname(self):
        abs_root = os.path.abspath(self.root)
        abs_fname = os.path.abspath(os.path.join(self.root, "%s.conf" % self.name))
        cpfx = os.path.commonprefix([abs_root, abs_fname])

        if len(cpfx) < len(abs_root):
            raise ParseError("You cannot attempt to include files from "
                             "outside the envmgr root (%s)"
                             % abs_fname)

        return abs_fname
