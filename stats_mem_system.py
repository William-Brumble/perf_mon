
import psutil
import traceback

from stats_abc import StatsAbc
from logger_csv import AppLogger

class MemSystemStats(StatsAbc):
    """ Responsible for getting system memory statistics. """
    def __init__(self, pApp_logger:AppLogger):
        super().__init__()
        self.logger = pApp_logger

    def __str__(self) -> str:
        return "MEMORY System Statistics Object"

    def get_stats(self, pDictionary:dict) -> dict:
        """ Get memory system statistics. """

        pDictionary = self._get_mem_percentage_system(pDictionary)

        return pDictionary

    def _get_mem_percentage_system(self, pDictionary:dict) -> dict:
        """ Get percentage of memory used. """
        try:
            memory_stats = psutil.virtual_memory()._asdict().get("percent", "")

            self.logger.log_info(f"- Getting memory usage percentage")
            pDictionary[f"mem_percentage_system"] = memory_stats
        except:
            self.logger.log_error(f"Failed to get system memory percentage: {traceback.format_exc()}")

        return pDictionary

if __name__ == "__main__":
    raise Exception("This module is not meant to be ran as main.")
