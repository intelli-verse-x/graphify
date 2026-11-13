"""Keep the CommonJS parser fixture inert; never execute its JavaScript."""
from pathlib import Path
import unittest

EXPECTED = b"const { loadFoundation, validateConfig } = require('./foundation');\nconst utils = require('./utils');\nconst helper = require('./helpers').helperFn;\n\nfunction runDispatch() {\n  const cfg = loadFoundation({});\n  validateConfig(cfg);\n  utils.log('go');\n  helper();\n}\n\nmodule.exports = { runDispatch };\n"


def check_fixture_bytes(raw):
    if raw.replace(b"\r\n", b"\n") != EXPECTED:
        raise ValueError("CommonJS parser fixture differs from its reviewed declarations")


class FixtureIntegrity(unittest.TestCase):
    def test_actual_fixture_has_only_reviewed_parser_declarations(self):
        check_fixture_bytes((Path(__file__).parent / "fixtures/cjs_require.js").read_bytes())

    def test_appended_executable_tail_is_rejected_as_data(self):
        with self.assertRaises(ValueError):
            check_fixture_bytes(EXPECTED + b"\n(() => { throw new Error('untrusted tail'); })();\n")

    def test_tail_hidden_after_whitespace_is_rejected_as_data(self):
        with self.assertRaises(ValueError):
            check_fixture_bytes(EXPECTED.rstrip() + b" " * 512 + b"; process.exit(0);\n")


if __name__ == "__main__":
    unittest.main()
