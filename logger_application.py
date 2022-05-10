
import sys
import logging
import traceback
from logging.handlers import RotatingFileHandler

class AppLogger(object):
    """ Logs appplication related data to log files. """

    def __init__(self,
            pPath:str,
            pName:str,
            pMax_bytes:int,
            pCount:int,
            pSilence:bool):
        """
        arguments:
            pPath (str): Directory where csv data is stored
            pName (str): Name of file to store csv data
            pMax_bytes (int): Maximum bytes for single csv file
            pCount (int): Number of rotating files to store data in
            pSilence: (bool): Whether or not to log app info to file
        """

        self.log_path = pPath + pName
        self.silence = pSilence
        self.logger = logging.getLogger("application_logger")
        self.logger.setLevel(logging.DEBUG)
        self.handler = RotatingFileHandler(self.log_path, maxBytes=pMax_bytes, backupCount=pCount)
        format = logging.Formatter(fmt="[%(asctime)s.%(msecs)03d] [%(levelname)s]: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        self.handler.setFormatter(format)
        self.logger.addHandler(self.handler)

    def log_info(self, pMessage:str) -> None:
        # Write info message to log file.

        if not self.silence:
            try: # Write message to the file
                self.logger.info(pMessage.upper())
            except:
                self.log_error(f"Failed to log app data to csv file: {traceback.format_exc()}")

    def log_error(self, pMessage:str) -> None:
        # Write error message to log file.

        try: # Write message to the file
            self.logger.error(pMessage.upper())
        except:
            sys.exit("Can not log error data, we are leaving now.")

if __name__ == "__main__":
    print("This module is not meant to be ran as main")

