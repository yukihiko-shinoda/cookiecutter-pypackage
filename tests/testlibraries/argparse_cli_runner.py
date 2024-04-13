"""CLI Runner for argparse."""

from argparse import ArgumentParser, Namespace
import sys
from typing import (
    Any,
    Callable,
    cast,
    Dict,
    IO,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    TYPE_CHECKING,
    Union,
)

from click.testing import CliRunner, Result
import pytest
from pytest_mock import MockerFixture

if TYPE_CHECKING:
    from types import TracebackType


class PartialMockArgumentParser:
    """Partial mock for ArgumentParser."""

    def __init__(self) -> None:
        self.argument_parser = ArgumentParser()
        self.args: Sequence[str] = []

    def parse_args(self) -> Namespace:
        if "--help" in self.args:
            return self.argument_parser.parse_args(self.args)
        args: Dict[str, List[Any]] = {arg: [] for arg in self.args}
        return Namespace(**args)


class ArgparseCliRunnerCore:
    """Core process of CLI Runner for argparse.

    This class is designed to recreate every time when invoke.
    """

    def __init__(
        self,
        mocker: MockerFixture,
        args: Union[str, Sequence[str], None],
        partial_mock: PartialMockArgumentParser,
    ) -> None:
        self.exc_info: Optional[
            Union[
                Tuple[Type[BaseException], BaseException, "TracebackType"],
                Tuple[None, None, None],
            ]
        ] = None
        self.return_value = None
        self.exception: Optional[BaseException] = None
        self.exit_code = 0
        mock = mocker.MagicMock()
        partial_mock.args = (
            [] if args is None else [args] if isinstance(args, str) else args
        )
        mock.return_value = partial_mock
        mocker.patch("argparse.ArgumentParser", mock)

    def invoke(
        self,
        cli: Callable[[], None],
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
    # pylint: disable=too-many-arguments,redefined-builtin
    def invoke(  # noqa: PLR0913
        self,
        cli: Callable[[], None],
        args: Union[str, Sequence[str], None] = None,
        input: Optional[Union[str, bytes, IO[Any]]] = None,  # noqa: A002,ARG002
        env: Optional[Mapping[str, Optional[str]]] = None,  # noqa: ARG002
        catch_exceptions: bool = True,  # noqa: ARG002,FBT001,FBT002
        color: bool = False,  # noqa: ARG002,FBT001,FBT002
        **extra: Any,  # noqa: ARG002
    ) -> Result:
        argparse_cli_runner_core = ArgparseCliRunnerCore(
            self.mocker,
            args,
            self.partial_mock,
        )
        return argparse_cli_runner_core.invoke(cli, self.capsys, self)
