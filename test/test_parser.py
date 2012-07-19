import os
import unittest

from envmgr.parser import EnvConfParser, ParseError

FIXTURES = os.path.join(os.path.dirname(__file__), 'fixtures')


class TestEnvConfParser(unittest.TestCase):
    def test_defaults_to_python_env(self):
        p = EnvConfParser('foo', 'root')
        self.assertEqual(p.env, os.environ)

    def test_start(self):
        p = EnvConfParser('foo', 'root', {'bar': 'baz'})
        self.assertEqual(p.env['bar'], 'baz')

    def test_simple(self):
        p = EnvConfParser('simple', FIXTURES, {})
        r = p.parse()
        self.assertEqual(r, {'FOO': 'bar', 'BAR': 'baz', 'BAZ': 'bat'})

    def test_clear_alone(self):
        p = EnvConfParser('clear_alone', FIXTURES, {'FOO': 'bar'})
        r = p.parse()
        self.assertEqual(r, {})

    def test_clear_order(self):
        p = EnvConfParser('clear_order', FIXTURES, {})
        r = p.parse()
        self.assertEqual(r, {'BAR': 'baz'})

    def test_unset(self):
        p = EnvConfParser('unset', FIXTURES, {'FOO': 'bar', 'BAR': 'baz'})
        r = p.parse()
        self.assertEqual(r, {'FOO': 'bar'})

    def test_include(self):
        p = EnvConfParser('include', FIXTURES, {})
        r = p.parse()
        self.assertEqual(r, {'FOO': 'bar', 'BAR': 'baz'})

    def test_parse_error(self):
        p = EnvConfParser('parse_error', FIXTURES, {})
        self.assertRaises(ParseError, p.parse)
