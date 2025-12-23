"""Robot connection wrapper for Reachy Mini."""

from contextlib import contextmanager
from typing import Generator

from reachy_mini import ReachyMini


class RobotConnectionError(Exception):
    """Raised when unable to connect to the robot."""

    pass


@contextmanager
def get_robot_connection(
    robot_name: str = "reachy_mini",
    localhost_only: bool = False,
    timeout: float = 5.0,
) -> Generator[ReachyMini, None, None]:
    """
    Context manager for connecting to Reachy Mini.

    Args:
        robot_name: Name of the robot for discovery.
        localhost_only: If True, only connect to localhost daemons.
        timeout: Connection timeout in seconds.

    Yields:
        Connected ReachyMini instance.

    Raises:
        RobotConnectionError: If connection fails.
    """
    try:
        with ReachyMini(
            robot_name=robot_name,
            localhost_only=localhost_only,
            timeout=timeout,
        ) as mini:
            yield mini
    except Exception as e:
        raise RobotConnectionError(f"Failed to connect to robot: {e}") from e
