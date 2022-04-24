
import time
import psutil
import traceback

from stats_abc import StatsAbc
from logger_csv import AppLogger

class DiskProcessStats(StatsAbc):
    """ Responsible for getting process disk statistics. """
    def __init__(self, pApp_logger:AppLogger, pProcess:psutil.Process = None):
        self.logger = pApp_logger
        self.process = pProcess
        self.io_counter_cache = {}

    def __str__(self) -> str:
        return f"DISK Process Statistics Object ({self.process.name()})"

    def get_stats(self, pDictionary:dict) -> dict:
        """ Get disk process statistics. """

        pDictionary = self._get_disk_io_counters(pDictionary)

        return pDictionary

    def _get_disk_io_counters(self, pDictionary:dict) -> dict:
        # Get disk process io counters.
        try:
            self.logger.log_info(f"- Getting system disk io counters from: ({self.process.name()}) process")
            disk_io_counters = self.process.io_counters()

            # Read in the raw accumulated read/write bytes
            cur_read_bytes = disk_io_counters._asdict().get("read_bytes", "")
            cur_write_bytes = disk_io_counters._asdict().get("write_bytes", "")

            # Calculate human readable per second values for read/write
            if self.io_counter_cache:
                # Get the cached values
                prev_read_bytes = self.io_counter_cache.get(f"disk_read_bytes_process", 0)
                prev_write_bytes = self.io_counter_cache.get(f"disk_write_bytes_process", 0)
                prev_read_write_time = self.io_counter_cache.get(f"disk_write_read_process", 1)

                # Calculate the speed
                read_per_sec = (cur_read_bytes - prev_read_bytes) / (time.perf_counter() - prev_read_write_time)
                write_per_sec = (cur_write_bytes - prev_write_bytes) / (time.perf_counter() - prev_read_write_time)

                # Output the values for historical logging
                pDictionary[f"disk_read_bytes_process"] = read_per_sec
                pDictionary[f"disk_write_bytes_process"] = write_per_sec
            else:
                # If we haven't cached values, set value to NAN
                pDictionary[f"disk_read_bytes_process"] = None
                pDictionary[f"disk_write_bytes_process"] = None

            # Cache for calculating per/sec values next time
            self.io_counter_cache[f"disk_read_bytes_process"] = cur_read_bytes
            self.io_counter_cache[f"disk_write_bytes_process"] = cur_write_bytes
            self.io_counter_cache[f"disk_write_read_time"] = time.perf_counter()
        except:
            self.logger.log_error(f"Failed to get process ({self.process.name()}) disk io counters: {traceback.format_exc()}")

        return pDictionary

if __name__ == "__main__":
    raise Exception("This module is not meant to be ran as main.")
