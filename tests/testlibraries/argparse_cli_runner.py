"""CLI Runner for argparse."""
import sys
from argparse import ArgumentParser, Namespace
from typing import Any, Optional, Union, cast

from click.testing import CliRunner, Result


class PartialMockArgumentParser:
    """Partial mock for ArgumentParser."""

    def __init__(self) -> None:
        self.argument_parser = ArgumentParser()
        self.args = None

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, value):
        self._args = [] if value is None else value

    def parse_args(self):
        if "--help" in self._args:
            return self.argument_parser.parse_args(self._args)
        args = {arg: [] for arg in self._args}
        return Namespace(**args)


class ArgparseCliRunnerCore:
    """Core process of CLI Runner for argparse.

    This class is designed to recreate every time when invoke.
    """

    def __init__(self, mocker, args, partial_mock) -> None:
        self.exc_info = None
        self.return_value = None
        self.exception = None
        self.exit_code = 0
        mock = mocker.MagicMock()
        partial_mock.args = args
        mock.return_value = partial_mock
        mocker.patch("argparse.ArgumentParser", mock)

    def invoke(self, cli, capsys, runner):
        """Invokes command."""
        try:
            self.return_value = cli()
        except SystemExit as error:
            self.exc_info = sys.exc_info()
            self.set_properties(error)
        # Reason: To extract exception information.
        except Exception as error:  # pylint: disable=broad-except
            self.exception = error
            self.exit_code = 1
            self.exc_info = sys.exc_info()
        finally:
            sys.stdout.flush()
            captured = capsys.readouterr()
            stdout = captured.out
            stderr = captured.err

        return Result(
            runner=runner,
            stdout_bytes=bytes(stdout, "utf-8"),
            stderr_bytes=bytes(stderr, "utf-8"),
            return_value=self.return_value,
            exit_code=self.exit_code,
            exception=self.exception,
            exc_info=self.exc_info,  # type: ignore
        )

    def set_properties(self, error):
        """Sets properties from SystemExit."""
        e_code = cast(Optional[Union[int, Any]], error.code)

        if e_code is None:
            e_code = 0

        if e_code != 0:
            self.exception = error

        if not isinstance(e_code, int):
            sys.stdout.write(str(e_code))
            sys.stdout.write("\n")
            e_code = 1

        self.exit_code = e_code


class ArgparseCliRunner(CliRunner):
    """CLI Runner for argparse."""

    def __init__(self, capsys, mocker) -> None:
        self.capsys = capsys
        self.mocker = mocker
        self.partial_mock = PartialMockArgumentParser()
        super().__init__()

    # Reason: Inherit design of parent class.
    # pylint: disable=too-many-arguments,redefined-builtin
    def invoke(
        self,
        cli,
        args=None,
        input=None,
        env=None,
        catch_exceptions=True,
        color=False,
        **extra
    ):
        argparse_cli_runner_core = ArgparseCliRunnerCore(
            self.mocker, args, self.partial_mock
        )
        return argparse_cli_runner_core.invoke(cli, self.capsys, self)
