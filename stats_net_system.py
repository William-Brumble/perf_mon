
import time
import psutil
import traceback

from stats_abc import StatsAbc
from logger_csv import AppLogger

class NetSystemStats(StatsAbc):
    """ Responsible for getting system network statistics. """
    def __init__(self, pApp_logger:AppLogger):
        super().__init__()
        self.logger = pApp_logger
        self.io_counter_cache = {}

    def __str__(self) -> str:
        return "NETWORK System Statistics Object"

    def get_stats(self, pDictionary:dict) -> dict:
        """ Get network system statistics. """
        pDictionary = self._get_net_io_counters(pDictionary)

        return pDictionary

    def _get_net_io_counters(self, pDictionary:dict) -> dict:
        """ Get net system io counters. """
        try:
            net_io_counters = psutil.net_io_counters(pernic=True, nowrap=True)

            for nic in net_io_counters.keys():
                self.logger.log_info(f"- Getting system io counters from: ({nic}) nic")

                # Read in the raw accumulated read/write bytes
                cur_bytes_recv = net_io_counters[nic]._asdict().get("bytes_recv", "")
                cur_bytes_sent = net_io_counters[nic]._asdict().get("bytes_sent", "")

                # Calculate human readable per second values for read/write
                if self.io_counter_cache:
                    # Get the cached values
                    prev_bytes_recv = self.io_counter_cache.get(f"net_({nic})_bytes_recv_system", 0)
                    prev_bytes_sent = self.io_counter_cache.get(f"net_({nic})_bytes_sent_system", 0)
                    prev_bytes_sent_recv = self.io_counter_cache.get(f"net_({nic})_sent_recv_time", 1)

                    # Calculate the speed
                    recv_per_sec = (cur_bytes_recv - prev_bytes_recv) / (time.perf_counter() - prev_bytes_sent_recv)
                    sent_per_sec = (cur_bytes_sent - prev_bytes_sent) / (time.perf_counter() - prev_bytes_sent_recv)

                    # Output the values for historical logging
                    pDictionary[f"net_({nic})_bytes_recv_system"] = recv_per_sec
                    pDictionary[f"net_({nic})_bytes_sent_system"] = sent_per_sec
                else:
                    # If we haven't cached values, set value to NAN
                    pDictionary[f"net_({nic})_bytes_recv_system"] = None
                    pDictionary[f"net_({nic})_bytes_sent_system"] = None

                # Cache for calculating per/sec values next time
                self.io_counter_cache[f"disk_({nic})_bytes_recv_system"] = cur_bytes_recv
                self.io_counter_cache[f"disk_({nic})_bytes_sent_system"] = cur_bytes_sent
                self.io_counter_cache[f"disk_({nic})_sent_recv_time"] = time.perf_counter()
        except:
            self.logger.log_error(f"Failed to get system net io counters: {traceback.format_exc()}")

        return pDictionary

class NetProcessStats:
    """ Don't see a way to log per process network stats. """
    pass

if __name__ == "__main__":
    raise Exception("This module is not meant to be ran as main.")
