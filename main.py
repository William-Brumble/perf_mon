
import sys
import time
from filelock import FileLock, Timeout

from factory import Factory
from logger_application import AppLogger

def main():

    factory = Factory()

    # Getting configurations
    # -------------------------------------------------------------------------
    config = factory.create_configurator()

    scan_rate = int(config.get("main", "scan_rate"))

    path_data = config.get("paths", "log_data")
    path_app = config.get("paths", "log_app")

    name_data = config.get("filenames", "log_data")
    name_app = config.get("filenames", "log_app")

    logger_app_max_bytes = int(config.get("app_logger", "max_bytes"))
    logger_app_num_files = int(config.get("app_logger", "num_files"))
    logger_app_silence_logs = bool(int(config.get("app_logger", "silence_logs")))

    logger_data_max_bytes = int(config.get("data_logger", "max_bytes"))
    logger_data_num_files = int(config.get("data_logger", "num_files"))

    processes = []
    for s_name, p_name in config["processes"].items():
        processes.append(p_name)
    # -------------------------------------------------------------------------

    # Creating application logger
    # -------------------------------------------------------------------------
    app_logger = factory.create_app_logger(
        path_app,
        name_app,
        logger_app_max_bytes,
        logger_app_num_files,
        logger_app_silence_logs
    )
    app_logger.log_info("Application has started")
    # -------------------------------------------------------------------------

    # Creating stats controller
    # -------------------------------------------------------------------------
    app_logger.log_info("Creating stats controller")
    stats_controller = factory.create_stats_controller(app_logger)
    # -------------------------------------------------------------------------

    # Creating cpu loggers
    # -------------------------------------------------------------------------
    app_logger.log_info("Creating cpu loggers")
    cpu_sys_logger = factory.create_cpu_system_logger(app_logger)
    stats_controller.add_stats(cpu_sys_logger)

    for process_name in processes:
        cpu_proc_logger = factory.create_cpu_process_logger(app_logger, process_name)
        if cpu_proc_logger:
            stats_controller.add_stats(cpu_proc_logger)
    # -------------------------------------------------------------------------

    # Creating disk loggers
    # -------------------------------------------------------------------------
    app_logger.log_info("Creating disk logger")
    disk_sys_logger = factory.create_disk_system_logger(app_logger)
    stats_controller.add_stats(disk_sys_logger)

    for process_name in processes:
        disk_proc_logger = factory.create_disk_process_logger(app_logger, process_name)
        if disk_proc_logger:
            stats_controller.add_stats(disk_proc_logger)
    # -------------------------------------------------------------------------

    # Creating memory loggers
    # -------------------------------------------------------------------------
    app_logger.log_info("Creating memory logger")
    mem_sys_logger = factory.create_mem_system_logger(app_logger)
    stats_controller.add_stats(mem_sys_logger)

    for process_name in processes:
        mem_proc_logger = factory.create_mem_process_logger(app_logger, process_name)
        if mem_proc_logger:
            stats_controller.add_stats(mem_proc_logger)
    # -------------------------------------------------------------------------

    # Creating network logger
    # -------------------------------------------------------------------------
    app_logger.log_info("Creating network logger")
    net_sys_logger = factory.create_net_system_logger(app_logger)
    stats_controller.add_stats(net_sys_logger)
    # -------------------------------------------------------------------------

    # Creating csv logger
    # -------------------------------------------------------------------------
    app_logger.log_info("Creating csv logger")
    csv_logger = factory.create_csv_logger(
        app_logger,
        path_data,
        name_data,
        logger_data_max_bytes,
        logger_data_num_files
    )
    # -------------------------------------------------------------------------

    # Using this to store a row of csv data
    stats_dictionary = {}

    # Programs main loop
    # -------------------------------------------------------------------------
    app_logger.log_info("Entering programs main loop")
    while True:
        app_logger.log_info("-" * 80)


        elapsed_time = 0
        tic = time.perf_counter()

        stats_dictionary = stats_controller.get_stats(stats_dictionary)

        app_logger.log_info("Writting statistics to csv file.")
        csv_logger.log_data(stats_dictionary)

        stats_dictionary.clear()

        toc = time.perf_counter()
        elapsed_time += toc - tic

        if elapsed_time < scan_rate:
            time.sleep(scan_rate - elapsed_time)
            elapsed_time += time.perf_counter() - toc
            app_logger.log_info(f"- Elapsed time: ({elapsed_time}) seconds.")
        else:
            elapsed_time += time.perf_counter() - toc
            app_logger.log_info(f"- Elapsed time: ({elapsed_time}) seconds.")
    # -------------------------------------------------------------------------

if __name__ == "__main__":

    lock = FileLock("pid.lock")

    try: # Confirming that this is the only instance of this program
        with lock.acquire(timeout=10):
            main()
    except Timeout:
        sys.exit("Another instance of this program is running.")
    finally:
        lock.release()
