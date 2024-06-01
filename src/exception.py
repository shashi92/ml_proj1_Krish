import sys
from src.logger import logging

def error_message(error, error_details:sys):
    _,_,exc_tb = error_details.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_str = f"Error occurred in file: {file_name}, line no: {exc_tb.tb_lineno}, error: {str(error)}"
    # logging.info(error_str)
    return error_str

class CustomException(Exception):
    def __init__(self, error_msg, error_details:sys):
        super().__init__(error_msg)
        self.error_msg = error_message(error_msg, error_details)
    
    def __str__(self):
        return self.error_msg
