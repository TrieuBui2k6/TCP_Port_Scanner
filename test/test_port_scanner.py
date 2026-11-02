import contextlib
import io
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

# Add the project root to Python's module search path.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import main

class CheckPortTests(unittest.TestCase):
    """Tests for the check_port() function."""

    @patch("main.socket.socket")
    def test_returns_true_when_connection_succeeds(self, socket_factory):
        connection = socket_factory.return_value.__enter__.return_value
        connection.connect_ex.return_value = 0

        result = main.check_port("127.0.0.1", 80)

        self.assertTrue(result)
        connection.settimeout.assert_called_once_with(1)
        connection.connect_ex.assert_called_once_with(("127.0.0.1", 80))

    @patch("main.socket.socket")
    def test_returns_false_when_connection_fails(self, socket_factory):
        connection = socket_factory.return_value.__enter__.return_value
        connection.connect_ex.return_value = 111

        result = main.check_port("127.0.0.1", 81)

        self.assertFalse(result)

    @patch("main.socket.socket")
    def test_returns_false_when_socket_raises_oserror(self, socket_factory):
        socket_factory.side_effect = OSError("Network error")

        result = main.check_port("127.0.0.1", 80)

        self.assertFalse(result)


class MainTests(unittest.TestCase):
    """Tests for the command-line interface."""

    @patch("builtins.input", side_effect=["127.0.0.1", "80-81", "exit"])
    @patch("main.check_port", side_effect=[True, False])
    def test_scans_range_and_reports_open_ports(
        self, mocked_check_port, mocked_input
    ):
        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            main.main()

        text = output.getvalue()

        self.assertIn(
            "Scanning 127.0.0.1, ports 80-81...",
            text,
        )
        self.assertIn(
            "Port 80 is open on 127.0.0.1.",
            text,
        )
        self.assertIn(
            "Open ports on 127.0.0.1: 80",
            text,
        )
        self.assertEqual(mocked_check_port.call_count, 2)

    @patch("builtins.input", side_effect=["127.0.0.1", "80-81", "exit"])
    @patch("main.check_port", return_value=False)
    def test_reports_when_no_open_ports_are_found(
        self, mocked_check_port, mocked_input
    ):
        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            main.main()

        self.assertIn(
            "No open ports found in the specified range.",
            output.getvalue(),
        )

    @patch("builtins.input", side_effect=["127.0.0.1", "70000-70001", "exit"])
    def test_rejects_out_of_range_ports(self, mocked_input):
        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            main.main()

        self.assertIn(
            "Invalid port range.",
            output.getvalue(),
        )


if __name__ == "__main__":
    unittest.main()