import logging
from pathlib import Path

from intraday_trend.src.exceptions import DirectoryError

logger = logging.getLogger(__name__)


class _Directories:
    def __init__(self):
        self.project = Path(__file__).parents[2].resolve()
        logger.info(f"Setting up directories at {self.project}")
        self.config = self.project / "config"
        self.package = self.project / "src"
        self.data = self.package / "data"
        self.price_data = self.data / "prices"
        self.pnl_data = self.data / "pnl"

        for dir_path in vars(self).values():
            try:
                dir_path.mkdir(exist_ok=True, parents=True)
            except Exception as e:
                # NOTE: could we just silently logger.error?
                raise DirectoryError(
                    f"Either '{dir_path}' is not a directory, "
                    "or it can't be created. "
                    f"Make sure all attributes of {self.__class__} "
                    "are actual directory paths."
                ) from e


directories = _Directories()
