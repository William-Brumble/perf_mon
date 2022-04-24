
from time import sleep
from os import mkdir, remove
from os.path import exists
from configparser import ConfigParser

class Configurator(ConfigParser):

    def __init__(self):
        super().__init__()
        if not exists("./config/"):
            mkdir("./config/")
        self.read("./config/configuration.ini")

    def write_settings(self) -> None:
        with open("./config/configuration.ini","w") as filename:
            self.write(filename)

if __name__ == "__main__":

    configure = True

    # Set the settings
    # -------------------------------------------------------------------------
    if configure:
        if exists("./config/configuration.ini"):
            remove("./config/configuration.ini")

        configurator = Configurator()

        configurator.add_section("main")
        configurator.set("main", "scan_rate", "1") # Log interval in seconds

        configurator.add_section("paths")
        configurator.set("paths", "log_data", "./data_sets/") # CSV data output directory
        configurator.set("paths", "log_app", "./logs/") # Application log output directory

        configurator.add_section("filenames")
        configurator.set("filenames", "log_data", "data.log") # CSV data output file names
        configurator.set("filenames", "log_app", "app.log") # Application log output file name

        configurator.add_section("processes")
        configurator.set("processes", "name", "System Idle Process")
        #configurator.set("processes", "name", "INSERT_NAME_HERE")
        #configurator.set("processes", "name", "INSERT_NAME_HERE")
        # ...

        configurator.add_section("app_logger")
        configurator.set("app_logger", "max_bytes", "2000000") # Application information log file sizes
        configurator.set("app_logger", "num_files", "2") # Number of application information log files
        configurator.set("app_logger", "silence_logs", "0") # Log application data? 0 for no, 1 for yes

        configurator.add_section("data_logger")
        configurator.set("data_logger", "max_bytes", "2000000") # Resource log file sizes
        configurator.set("data_logger", "num_files", "500") # Number of resource log files

        configurator.write_settings()
    # -------------------------------------------------------------------------

    # View the settings
    # -------------------------------------------------------------------------
    else: 
        configurator = Configurator()

        print("Main settings:")
        for name, value in configurator["main"].items():
            print(name + " : " + value)

        print("Path settings:")
        for name, value in configurator["paths"].items():
            print(name + " : " + value)

        print("Filename settings:")
        for name, value in configurator["filenames"].items():
            print(name + " : " + value)

        print("Process settings:")
        for name, value in configurator["processes"].items():
            print(name + " : " + value)

        print("App logger settings:")
        for name, value in configurator["app_logger"].items():
            print(name + " : " + value)

        print("Data logger settings:")
        for name, value in configurator["data_logger"].items():
            print(name + " : " + value)
    # -------------------------------------------------------------------------
