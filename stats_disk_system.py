
import time
import psutil
import traceback

from stats_abc import StatsAbc
from logger_csv import AppLogger

class DiskSystemStats(StatsAbc):
    """ Responsible for getting system disk statistics. """
    def __init__(self, pApp_logger:AppLogger):
        super().__init__()
        self.logger = pApp_logger
        self.io_counter_cache = {}

    def __str__(self) -> str:
        return "DISK System Statistics Object"

    def get_stats(self, pDictionary:dict) -> dict:
        """ Get disk system statistics. """

        pDictionary = self._get_disk_usage_percent(pDictionary)
        pDictionary = self._get_disk_io_counters(pDictionary)

        return pDictionary

    def _get_disk_usage_percent(self, pDictionary:dict) -> dict:
        """ Get disk system percentage. """
        try:
            for disk in psutil.disk_partitions(all=False):
                disk_usage_percent = psutil.disk_usage(disk.mountpoint)._asdict().get("percent", "")

                self.logger.log_info(f"- Getting disk usage percentage from: ({disk.mountpoint}) path")
                pDictionary[f"disk_usage_percent_({disk.mountpoint})"] = disk_usage_percent
        except:
            self.logger.log_error(f"Failed to get system disk usage percent: {traceback.format_exc()}")

        return pDictionary

    def _get_disk_io_counters(self, pDictionary:dict) -> dict:
        """ Get disk system io counters. """
        try:
            disk_io_counters = psutil.disk_io_counters(perdisk=True, nowrap=True)

            for disk in disk_io_counters.keys():
                self.logger.log_info(f"- Getting system disk io counters from: ({disk}) disk")
                # Read in the raw accumulated read/write bytes
                cur_read_bytes = disk_io_counters[disk]._asdict().get("read_bytes", "")
                cur_write_bytes = disk_io_counters[disk]._asdict().get("write_bytes", "")

                # Calculate human readable per second values for read/write
                if self.io_counter_cache:
                    # Get the cached values
                    prev_read_bytes = self.io_counter_cache.get(f"disk_({disk})_read_bytes_system", 0)
                    prev_write_bytes = self.io_counter_cache.get(f"disk_({disk})_write_bytes_system", 0)
                    prev_read_write_time = self.io_counter_cache.get(f"disk_({disk})_write_read_time", 1)

                    # Calculate the speed
                    read_per_sec = (cur_read_bytes - prev_read_bytes) / (time.perf_counter() - prev_read_write_time)
                    write_per_sec = (cur_write_bytes - prev_write_bytes) / (time.perf_counter() - prev_read_write_time)

                    # Output the values for historical logging
                    pDictionary[f"disk_({disk})_read_bytes_system"] = read_per_sec
                    pDictionary[f"disk_({disk})_write_bytes_system"] = write_per_sec
                else:
                    # If we haven't cached values, set value to NAN
                    pDictionary[f"disk_({disk})_read_bytes_system"] = None
                    pDictionary[f"disk_({disk})_write_bytes_system"] = None

                # Cache for calculating per/sec values next time
                self.io_counter_cache[f"disk_({disk})_read_bytes_system"] = cur_read_bytes
                self.io_counter_cache[f"disk_({disk})_write_bytes_system"] = cur_write_bytes
                self.io_counter_cache[f"disk_({disk})_write_read_time"] = time.perf_counter()
        except:
            self.logger.log_error(f"Failed to get system disk io counters: {traceback.format_exc()}")

        return pDictionary

if __name__ == "__main__":
    raise Exception("This module is not meant to be ran as main.")
