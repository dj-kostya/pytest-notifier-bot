import pytest
"""Submit failure or test session information to a pastebin service."""
import tempfile
from io import StringIO
import os
import sys
from typing import IO
from typing import Union

import pytest
from _pytest.config import Config
from _pytest.config import create_terminal_writer
from _pytest.config.argparsing import Parser
from _pytest.stash import StashKey
from _pytest.terminal import TerminalReporter


def pytest_terminal_summary(terminalreporter: TerminalReporter) -> None:
    if terminalreporter.config.option.pastebin != "failed":
        return
    if "failed" in terminalreporter.stats:
        terminalreporter.write_sep("=", "Sending information to Paste Service")
        for rep in terminalreporter.stats["failed"]:
            try:
                msg = rep.longrepr.reprtraceback.reprentries[-1].reprfileloc
            except AttributeError:
                msg = terminalreporter._getfailureheadline(rep)
            file = StringIO()
            tw = create_terminal_writer(terminalreporter.config, file)
            rep.toterminal(tw)
            s = file.getvalue()
            assert len(s)
            print(f"{msg}")

if __name__=='__main__':
    m_path = "pytest"

    #pytest.main(["--md-report", "--md-report-verbose", "3", "pytest/"])
    pytest.main(["--failed", "\pytest"])
