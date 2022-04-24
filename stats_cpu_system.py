
import psutil
import traceback

from stats_abc import StatsAbc
from logger_csv import AppLogger

class CpuSystemStats(StatsAbc):
    """ Responsible for getting system cpu statistics. """
    def __init__(self, pApp_logger:AppLogger):
        super().__init__()
        self.logger = pApp_logger

    def __str__(self) -> str:
        return "CPU System Statistics Object"

    def get_stats(self, pDictionary:dict) -> dict:
        """ Get cpu system statistics. """

        pDictionary = self._get_cpu_count_system(pDictionary)
        pDictionary = self._get_cpu_percentage_system(pDictionary)
        pDictionary = self._get_cpu_times_percentage_system(pDictionary)
        pDictionary = self._get_cpu_stats_system(pDictionary)
        pDictionary = self._get_cpu_frequency_system(pDictionary)
        pDictionary = self._get_cpu_load_average_system(pDictionary)

        return pDictionary

    def _get_cpu_count_system(self, pDictionary:dict) -> dict:
        """ Get the number of logical cpu cores. """
        try:
            self.logger.log_info("- Getting cpu count")
            cpu_count = psutil.cpu_count()

            pDictionary[f"cpu_count_system"] = cpu_count
        except:
            self.logger.log_error(f"Failed to get system cpu count: {traceback.format_exc()}")

        return pDictionary

    def _get_cpu_stats_system(self, pDictionary:dict) -> dict:
        """ Get cpu statistics (numbers are since boot). """
        try:
            cpu_stats = psutil.cpu_stats()

            for key, value in cpu_stats._asdict().items():
                self.logger.log_info(f"- Getting cpu stat from: ({key}) scope")
                pDictionary[f"cpu_stats_({key})_system"] = value
        except:
            self.logger.log_error(f"Failed to get system cpu stats: {traceback.format_exc()}")

        return pDictionary

    def _get_cpu_percentage_system(self, pDictionary:dict) -> dict:
        """ Get cpu percentage per cpu thread. """
        try:
            cpu_percent_system = psutil.cpu_percent(interval=None, percpu=True)

            for index, percent in enumerate(cpu_percent_system):
                self.logger.log_info(f"- Getting cpu perc from: ({index}) core")
                pDictionary[f"cpu_percent_core_({index + 1})_system"] = percent
        except:
            self.logger.log_error(f"Failed to get system cpu percentage: {traceback.format_exc()}")

        return pDictionary

    def _get_cpu_times_percentage_system(self, pDictionary:dict) -> dict:
        """ Get cpu times percentage per cpu thread. """
        try:
            cores = psutil.cpu_times_percent(interval=None, percpu=True)

            for index, core in enumerate(cores):
                for key, value in core._asdict().items():
                    self.logger.log_info(f"- Getting cpu time percentage from: ({index + 1}) core, ({key}) scope")
                    pDictionary[f"cpu_times_percent_core_({index + 1})_({key})_system"] = value
        except:
            self.logger.log_error(f"Failed to get system cpu times percentages: {traceback.format_exc()}")

        return pDictionary

    def _get_cpu_frequency_system(self, pDictionary:dict) -> dict:
        """ Get cpu times percentage per cpu thread. Linux supports multiple cores, winblows does not. """
        try:
            frequencies = psutil.cpu_freq(percpu=True)

            for index, frequency in enumerate(frequencies):
                for key, value in frequency._asdict().items():
                    # ignore min/max, will do this when charting data
                    if key == "min":
                        continue
                    elif key == "max":
                        continue
                    else:
                        self.logger.log_info(f"- Getting cpu frequency from: ({index + 1}) core")
                        pDictionary[f"cpu_frequency_core_({index + 1})_({key})_system"] = value
        except:
            self.logger.log_error(f"Failed to get system cpu frequency: {traceback.format_exc()}")

        return pDictionary

    def _get_cpu_load_average_system(self, pDictionary:dict) -> dict:
        """ Get cpu load_averages 1, 5, and 15 minutes. """
        try:
            self.logger.log_info(f"- Getting cpu load averages")
            avg = [x / psutil.cpu_count() * 100 for x in psutil.getloadavg()]

            pDictionary[f"cpu_load_average_1_min_system"] = avg[0]
            pDictionary[f"cpu_load_average_5_min_system"] = avg[1]
            pDictionary[f"cpu_load_average_15_min_system"] = avg[2]
        except:
            self.logger.log_error(f"Failed to get system cpu load averages: {traceback.format_exc()}")

        return pDictionary

if __name__ == "__main__":
    raise Exception("This module is not meant to be ran as main.")
