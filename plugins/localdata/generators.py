from typing import Dict, List
import logging
import pathlib
import json
import glob
import os

from pelican.generators import Generator

__all__ = ["JsonDataGenerator"]


logger = logging.getLogger(__name__)


class PluginDataException(Exception):
    pass


class JsonDataGenerator(Generator):
    """Load data from JSON files"""

    CONTEXT_PREFIX = "DATA_"

    def __init__(
        self,
        context,
        settings,
        path,
        theme,
        output_path,
        readers_cache_name="",
        **kwargs,
    ):
        super().__init__(
            context,
            settings,
            path,
            theme,
            output_path,
            readers_cache_name=readers_cache_name,
            **kwargs,
        )
        self.settings.setdefault("DATA_PATH", "data")
        logger.info("PLUGIN: init data plugins")

    def _find_files(self) -> List[str]:
        """Find all the JSON files in the DATA_PATH directory"""

        data_dir = pathlib.Path(self.settings["DATA_PATH"])

        # turn path into absolute if not already
        if not data_dir.is_absolute():
            data_dir = pathlib.Path(self.settings["PATH"]).joinpath(data_dir)

        if not data_dir.exists():
            raise PluginDataException(f"DATA_PATH {data_dir} path does not exist")

        if not data_dir.is_dir():
            raise PluginDataException(f"DATA_PATH {data_dir} path is not a directory")

        return glob.glob(os.path.join(data_dir, "**/*.json"), recursive=True)

    def generate_context(self):
        """Generate context from data files"""
        files = self._find_files()
        logger.debug("Matched files:\n%s", "\n".join(files))

        for file in files:
            name: str = _normalize_filename(file)
            data: Dict = _parse_file(file)
            self.context[self.CONTEXT_PREFIX + name] = data
            logger.info(
                "%s available inside template as '%s'", file, self.CONTEXT_PREFIX + name
            )


def _normalize_filename(file: str) -> str:
    return (
        os.path.basename(file).split(".")[0].replace(".", "_").replace("-", "_").upper()
    )


def _parse_file(filepath: str):
    """Parse data from file"""
    with open(filepath, "r") as fd:
        try:
            return json.load(fd)
        except ValueError as err:
            raise ValueError("failed to parse %s" % filepath) from err
