
import psutil
import traceback
from os import mkdir
from os.path import exists
from typing import List, Tuple

from logger_csv import CsvLogger, AppLogger
from configurator import Configurator
from stats_controller import StatsController
from stats_cpu_system import CpuSystemStats
from stats_cpu_process import CpuProcessStats
from stats_disk_system import DiskSystemStats
from stats_disk_process import DiskProcessStats
from stats_mem_system import MemSystemStats
from stats_mem_process import MemProcessStats
from stats_net_system import NetSystemStats

class Factory(object):

    def __init__(self):
        self.logger = None

    def create_app_logger(self,
                    pPath:str,
                    pName:str,
                    pMax_bytes:int,
                    pCount:int,
                    pSilence:bool) -> AppLogger:
        app_logger = AppLogger(
            pPath,
            pName,
            pMax_bytes,
            pCount,
            pSilence
        )
        self.logger = app_logger
        return app_logger

    def create_directories(self, pDirectories:List[str]) -> None:
        for directory in pDirectories:
            if not exists(directory):
                mkdir(directory)

    def create_configurator(self,) -> CsvLogger:
        configurator = Configurator()
        return configurator

    def create_stats_controller(self, pApp_logger:AppLogger) -> StatsController:
        stats_controller = StatsController(pApp_logger)
        return stats_controller

    def create_cpu_system_logger(self, pApp_logger:AppLogger) -> CpuSystemStats:
        cpu_system = CpuSystemStats(pApp_logger)
        return cpu_system

    def create_cpu_process_logger(self, pApp_logger:AppLogger, pProcess_name:str) -> Tuple[CpuProcessStats, None]:
        pid = self._find_process(pProcess_name)
        if pid:
            try:
                process = psutil.Process(pid=pid)
                cpu_process = CpuProcessStats(pApp_logger, process)
                return cpu_process
            except psutil.NoSuchProcess:
                self.logger.log_error(f"Failed to create cpu process ({pProcess_name}) {traceback.format_exc()}")
        else:
            return None

    def create_disk_system_logger(self, pApp_logger:AppLogger) -> DiskSystemStats:
        disk_system = DiskSystemStats(pApp_logger)
        return disk_system

    def create_disk_process_logger(self, pApp_logger:AppLogger, pProcess_name:str) -> Tuple[DiskProcessStats, None]:
        pid = self._find_process(pProcess_name)
        if pid:
            try:
                process = psutil.Process(pid=pid)
                disk_process = DiskProcessStats(pApp_logger, process)
                return disk_process
            except psutil.NoSuchProcess:
                self.logger.log_error(f"Failed to create disk process ({pProcess_name}) {traceback.format_exc()}")
        else:
            return None

    def create_mem_system_logger(self, pApp_logger:AppLogger) -> MemSystemStats:
        mem_system = MemSystemStats(pApp_logger)
        return mem_system

    def create_mem_process_logger(self, pApp_logger:AppLogger, pProcess_name:str) -> Tuple[MemProcessStats, None]:
        pid = self._find_process(pProcess_name)
        if pid:
            try:
                process = psutil.Process(pid=pid)
                mem_process = MemProcessStats(pApp_logger, process)
                return mem_process
            except psutil.NoSuchProcess:
                self.logger.log_error(f"Failed to create mem process ({pProcess_name}) {traceback.format_exc()}")
        else:
            return None

    def create_net_system_logger(self, pApp_logger:AppLogger) -> NetSystemStats:
        net_system = NetSystemStats(pApp_logger)
        return net_system

    def create_csv_logger(self, 
                    pApp_logger:AppLogger,
                    pPath:str,
                    pName:str,
                    pMax_bytes:int,
                    pCount:int) -> CsvLogger:
        csv_logger = CsvLogger(
            pApp_logger,
            pPath,
            pName,
            pMax_bytes,
            pCount,
        )
        return csv_logger

    def _find_process(self, pName:str) -> Tuple[int, None]:
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info.get("name") == pName:
                return proc.info.get("pid")
        return None
