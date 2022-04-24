
import psutil
import traceback

from stats_abc import StatsAbc
from logger_csv import AppLogger

class CpuProcessStats(StatsAbc):
    """ Responsible for getting process cpu statistics. """
    def __init__(self, pApp_logger:AppLogger, pProcess:psutil.Process = None):
        self.logger = pApp_logger
        self.process = pProcess

    def __str__(self) -> str:
        return f"CPU Process Statistics Object ({self.process.name()})"

    def get_stats(self, pDictionary:dict) -> dict:
        """ Get process cpu statistics. """

        pDictionary = self._get_cpu_times_process(pDictionary)
        pDictionary = self._get_cpu_percentage_process(pDictionary)

        return pDictionary

    def _get_cpu_times_process(self, pDictionary:dict) -> dict:
        """ Get cpu times for the process. """
        try:
            with self.process.oneshot():
                cpu_times = self.process.cpu_times()

            for key, value in cpu_times._asdict().items():
                self.logger.log_info(f"- Getting cpu times from: ({self.process.name()}) process, ({key}) scope")
                pDictionary[f"cpu_times_({key})_process_({self.process.name()})"] = value
        except:
            self.logger.log_error(f"Failed to get process ({self.process.name()}) cpu times: {traceback.format_exc()}")

        return pDictionary

    def _get_cpu_percentage_process(self, pDictionary:dict) -> dict:
        """ Get cpu times for the process, just like UNIX top this is not evenly accross threads. """
        try:
            with self.process.oneshot():
                cpu_percent = self.process.cpu_percent()

            self.logger.log_info(f"- Getting cpu usage percentage from: ({self.process.name()}) process")
            pDictionary[f"cpu_percent_process_({self.process.name()})"] = cpu_percent
        except:
            self.logger.log_error(f"Failed to get process ({self.process.name()}) cpu percentages: {traceback.format_exc()}")

        return pDictionary

if __name__ == "__main__":
    raise Exception("This module is not meant to be ran as main.")
