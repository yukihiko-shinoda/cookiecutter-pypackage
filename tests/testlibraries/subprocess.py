"""To run command in subprocess."""
import shlex

# Reason: Accept risk of using subprocess.
from subprocess import CalledProcessError, PIPE, run  # nosec B404


def run_subrocess(command: str) -> None:
    """To prevent to stop pytest process itself if raise some kind of interrupt."""
    try:
        # Reason: Accept risk of using subprocess.
        run(shlex.split(command), check=True, stdout=PIPE, stderr=PIPE)  # nosec B603
    except CalledProcessError as error:
        print(str(error.stdout).encode("ascii", "ignore").decode("unicode_escape"))
        print(str(error.stderr).encode("ascii", "ignore").decode("unicode_escape"))
        raise
