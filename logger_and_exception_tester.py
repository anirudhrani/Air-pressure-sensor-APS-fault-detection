from sensor.logger import logging
from sensor.exception import SensorException
import sys

def test_logger_exception():
    try: 
        logging.info('Starting the test_logger_exception.')
        result= 3/0
        print(result)
        logging.info('Ending the test_logger_exception.')
    except Exception as e:
        logging.debug('Terminating test_logger_exception. ')
        raise SensorException(e, sys)


if __name__== '__main__':
    try:
        test_logger_exception()
    except Exception as e:
        print(e)