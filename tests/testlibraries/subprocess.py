"""To run command in subprocess."""

import shlex
from logging import getLogger

# Reason: Accept risk of using subprocess.
from subprocess import CalledProcessError  # nosec B404
from subprocess import run  # nosec B404


def run_subprocess(command: str) -> None:
    """To prevent to stop pytest process itself if raise some kind of interrupt."""
    split_command = shlex.split(command)
    try:
        # Reason: Accept risk of using subprocess.
        run(split_command, check=True, capture_output=True)  # nosec B603 # noqa: S603
    except CalledProcessError as error:
        logger = getLogger(__name__)
        stdout = error.stdout.decode("utf-8", errors="replace") if error.stdout else ""
        logger.error("STDOUT:\n%s", stdout)
        stderr = error.stderr.decode("utf-8", errors="replace") if error.stderr else ""
        logger.error("STDERR:\n%s", stderr)
        raise
