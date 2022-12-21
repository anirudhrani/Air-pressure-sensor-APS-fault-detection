import sys

def error_message_detail(error, error_detail:sys): 

       # TRACEBACK -> Determination of the origin of the process.
       # sys.exc_info() method returns a tuple with three values (type, value, traceback)
    
        _,_, exc_tb= error_detail.exc_info()

        # Finding the path of the file where error occured.
        file_path= exc_tb.tb_frame.f_code.co_filename
        
        # exc_tb -> Gives the traceback of the error.
        # .tb_frame -> Gives the trace back and the absolute path with 2 slashes.
        # .f_code -> Give the trace back and the absolute path in a proper format (with 1 slash).
        # .co_filename -> Gives the absolute path of the traceback in a proper fromat.
        
        
        # Printing the error message.
        error_message= "Error occured in the script located at : [{0}] in line number [{1}] with error message [{2}]".format(
        file_path, exc_tb.tb_lineno, str(error))
        # tb_lineno -> Gives the line no.where the exception occurred.
        return error_message







class SensorException(Exception):
    def __init__(self,error_message, error_detail:sys):
        self.error_message = error_message_detail( error_message, error_detail= error_detail)

    def __str__(self):
        return self.error_message

   