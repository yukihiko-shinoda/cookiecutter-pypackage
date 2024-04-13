"""To run command in subprocess."""

from logging import getLogger
import shlex

# Reason: Accept risk of using subprocess.
from subprocess import CalledProcessError, run  # nosec B404


def run_subrocess(command: str) -> None:
    """To prevent to stop pytest process itself if raise some kind of interrupt."""
    split_command = shlex.split(command)
    try:
        # Reason: Accept risk of using subprocess.
        run(split_command, check=True, capture_output=True)  # nosec B603 # noqa: S603
    except CalledProcessError as error:
        logger = getLogger(__name__)
        stdout = str(error.stdout).encode("ascii", "ignore").decode("unicode_escape")
        logger.exception(stdout)
        stderr = str(error.stderr).encode("ascii", "ignore").decode("unicode_escape")
        logger.exception(stderr)
        raise
