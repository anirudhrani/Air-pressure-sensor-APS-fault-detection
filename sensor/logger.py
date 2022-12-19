import logging
from datetime import datetime
import os

# File name
FILE_NAME= f"{datetime.now().strftime('%m%d%Y__%H_%M_%S')}.log"

# Folder name
DIRECTORY_NAME= os.path.join(os.getcwd(), "logs")

# Creating a log folder if it does not exist.
os.makedirs(DIRECTORY_NAME, exist_ok= True)

# Path
DIRECTORY_PATH= os.path.join(DIRECTORY_NAME, FILE_NAME)

# Logging basic config
logging.basicConfig(
    filename= DIRECTORY_PATH,
    format= "[ %(asctime)s %(lineno)d %(name)s - %(levelname)s %(message)s]",
    level= logging.INFO,
)