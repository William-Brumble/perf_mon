
import psutil
import traceback

from stats_abc import StatsAbc
from logger_csv import AppLogger

class MemProcessStats(StatsAbc):
    """ Responsible for getting process memory statistics. """
    def __init__(self, pApp_logger:AppLogger, pProcess:psutil.Process = None):
        self.logger = pApp_logger
        self.process = pProcess

    def __str__(self) -> str:
        return f"MEMORY Process Statistics Object ({self.process.cmdline()})"

    def get_stats(self, pDictionary:dict) -> dict:
        """ Get process memory statistics. """

        pDictionary = self._get_memory_rss_percentage(pDictionary)
        pDictionary = self._get_memory_vms_percentage(pDictionary)

        return pDictionary

    def _get_memory_rss_percentage(self, pDictionary:dict) -> dict:
        """ Calculates memory percentage vs rss. """
        try:
            with self.process.oneshot():
                memory_percent = self.process.memory_percent(memtype="rss")

            self.logger.log_info(f"- Getting memory usage percentage from: ({'rss'}) scope, ({self.process.cmdline()}) process")
            pDictionary[f"memory_percent_rss_process_({self.process.cmdline()})"] = memory_percent
        except:
            self.logger.log_error(f"Failed to get process memory rss percentage: {traceback.format_exc()}")

        return pDictionary

    def _get_memory_vms_percentage(self, pDictionary:dict) -> dict:
        """ Calculates memory percentage vs vms. """
        try:
            with self.process.oneshot():
                memory_percent = self.process.memory_percent(memtype="vms")

            self.logger.log_info(f"- Getting memory usage percentage from: ({'vms'}) scope, ({self.process.cmdline()}) process")
            pDictionary[f"memory_percent_vms_process_({self.process.cmdline()})"] = memory_percent
        except:
            self.logger.log_error(f"Failed to get process memory vms percentage: {traceback.format_exc()}")

        return pDictionary

if __name__ == "__main__":
    raise Exception("This module is not meant to be ran as main.")
