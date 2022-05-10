
import pstats
import time
import traceback
from typing import List, Tuple

from stats_abc import StatsAbc
from logger_csv import AppLogger

class StatsController(object):
    """ Responsible for getting stats from all of the different stats objects. """

    def __init__(self, pApp_logger:AppLogger, pList:List[StatsAbc] = None):
        self.logger = pApp_logger
        self.stats = []

    def __str__(self) -> str:
        return "CONTROLLER Statistics Object"

    def add_stats(self, pStats:Tuple[List[StatsAbc], StatsAbc]) -> None:
        self.logger.log_info(f"Adding ({str(pStats)}) to stats controller")
        if isinstance(pStats, list):
            self.stats.extend(pStats)
        else:
            self.stats.append(pStats)

    def get_stats(self, pDictionary:dict) -> dict:
        try:
            for stat in self.stats:
                self.logger.log_info(f"Getting stats from: ({stat}) stats object")
                pDictionary = stat.get_stats(pDictionary)
        except:
            self.logger.log_error(f"Failed to get system statistics: {traceback.format_exc()}")

        return pDictionary

if __name__ == "__main__":
    print("This module is not meant to be ran as main")

