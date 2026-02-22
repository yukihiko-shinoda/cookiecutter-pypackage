"""CLI Runner for argparse."""

from __future__ import annotations

import sys
from argparse import ArgumentParser
from argparse import Namespace
from typing import IO
from typing import TYPE_CHECKING
from typing import Any
from typing import Callable
from typing import Mapping
from typing import Sequence
from typing import cast

from click.testing import CliRunner
from click.testing import Result

if TYPE_CHECKING:
    from types import TracebackType

    import pytest
    from pytest_mock import MockerFixture


class PartialMockArgumentParser:
    """Partial mock for ArgumentParser."""

    def __init__(self) -> None:
        self.argument_parser = ArgumentParser()
        self.args: Sequence[str] = []

    def parse_args(self) -> Namespace:
        if "--help" in self.args:
            return self.argument_parser.parse_args(self.args)
        args: dict[str, list[Any]] = {arg: [] for arg in self.args}
        return Namespace(**args)


class ArgparseCliRunnerCore:
    """Core process of CLI Runner for argparse.

    This class is designed to recreate every time when invoke.
    """

    def __init__(
        self,
        mocker: MockerFixture,
        args: str | Sequence[str] | None,
        partial_mock: PartialMockArgumentParser,
    ) -> None:
        self.exc_info: (
            tuple[type[BaseException], BaseException, TracebackType]
            | tuple[None, None, None]
            | None
        ) = None
        self.return_value: int | None = None
        self.exception: BaseException | None = None
        self.exit_code = 0
        mock = mocker.MagicMock()
        partial_mock.args = (
            [] if args is None else [args] if isinstance(args, str) else args
        )
        mock.return_value = partial_mock
        mocker.patch("argparse.ArgumentParser", mock)

    def invoke(
        self,
        cli: Callable[[], int],
        capsys: pytest.CaptureFixture[str],
        runner: CliRunner,
    ) -> Result:
        """Invokes command."""
        try:
            self.return_value = cli()
        except SystemExit as error:
            self.exc_info = sys.exc_info()
            self.set_properties(error)
        # Reason: To extract exception information.
        except Exception as error:  # pylint: disable=broad-except  # noqa: BLE001
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
            # Reason: Class: click.testing.CliRunner is doing so.
            exc_info=self.exc_info,  # type: ignore[arg-type]
        )

    def set_properties(self, error: SystemExit) -> None:
        """Sets properties from SystemExit."""
        e_code = cast("int | Any | None", error.code)

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

    def __init__(
        self,
        capsys: pytest.CaptureFixture[str],
        mocker: MockerFixture,
    ) -> None:
        self.capsys = capsys
        self.mocker = mocker
        self.partial_mock = PartialMockArgumentParser()
        super().__init__()

    # Reason: Inherit design of parent class.
    # pylint: disable-next=too-many-arguments,too-many-positional-arguments
    def invoke(  # noqa: PLR0913
        self,
        cli: Callable[[], int],
        args: str | Sequence[str] | None = None,
        # Reason: Inherit design of parent class.
        # pylint: disable-next=redefined-builtin
        input: str | bytes | IO[Any] | None = None,  # noqa: A002,ARG002
        env: Mapping[str, str | None] | None = None,  # noqa: ARG002
        catch_exceptions: bool | None = True,  # noqa: ARG002,FBT001,FBT002
        color: bool = False,  # noqa: ARG002,FBT001,FBT002
        **extra: Any,  # noqa: ARG002,ANN401
    ) -> Result:
        argparse_cli_runner_core = ArgparseCliRunnerCore(
            self.mocker,
            args,
            self.partial_mock,
        )
        return argparse_cli_runner_core.invoke(cli, self.capsys, self)
