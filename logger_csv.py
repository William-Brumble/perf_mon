
import logging
import traceback
from logging.handlers import RotatingFileHandler

from logger_application import AppLogger

class CsvLogger(object):
    """
    Logs performance data to csv files.

    public methods:
        log_data: Writes row of data to a csv file.
        write_header: Writes header information to csv file.
    """

    def __init__(self,
            pApp_logger:AppLogger,
            pPath:str,
            pName:str,
            pMax_bytes:int,
            pCount:int):
        """
        arguments:
            pApp_logger (AppLogger): Logger used to log information
            pPath (str): Directory where csv data is stored
            pName (str): Name of file to store csv data
            pMax_bytes (int): Maximum bytes for single csv file
            pCount (int): Number of rotating files to store data in
        """

        self.app_logger = pApp_logger
        self.log_path = pPath + pName
        self.logger = logging.getLogger("csv_logger")
        self.logger.setLevel(logging.INFO)
        self.handler = RotatingFileHandler(self.log_path, maxBytes=pMax_bytes, backupCount=pCount)
        format = logging.Formatter(fmt="%(asctime)s.%(msecs)03d, %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        self.handler.setFormatter(format)
        self.logger.addHandler(self.handler)

    def log_data(self, pDictionary:dict) -> None:
        """
        Writes row of data to the csv file.

        arguments:
            pDictionary (dict): Row of csv data
        """

        # Convert the dictionary values to a csv string
        data_list = [pDictionary.get(key, "") for key in pDictionary]
        data_csv_str = ", ".join(map(str, data_list))

        try: # Initial run write the headers
            if self.__class__.log_data.called:
                pass
        except AttributeError:
            self.app_logger.log_info("Initial run, generating csv header file")
            self.__class__.log_data.called = True
            self.write_header(pDictionary)
        
        try: # Write the data to the csv file
            self.logger.info(data_csv_str)
        except:
            self.app_logger.log_error(f"Failed to log data to csv file: {traceback.format_exc()}")

    def write_header(self, pDictionary) -> None:
        """
        Write headers, aka dict keys to the log file.

        arguments:
            pDictionary (dict): Row of csv headers
        """

        # Convert the dictionary values to a csv string
        header_list = [f'"{key}"' for key in pDictionary.keys()]
        header_csv_str = ", ".join(map(str, header_list))

        # Add time header to the beginning of the headers
        headers = '"time", ' + header_csv_str
        
        try: # Write the data to the csv file.
            with open(self.log_path + ".header", "w") as header_file:
                header_file.write(headers)
        except:
            self.app_logger.log_error(f"Failed to log headers to csv file: {traceback.format_exc()}")

if __name__ == "__main__":
    print("This module is not meant to be ran as main")
