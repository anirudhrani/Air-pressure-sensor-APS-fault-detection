# Setup.py -> It includes choices and metadata about the program, such as the package name, version, author, license, 
#             minimal dependencies, entry points, data files, and so on.
from setuptools import setup, find_packages
from typing import List



# find_packages -> Considers __init__.py file as packages.
# install_requires -> Installs required set of libraries curated by get_requirements function.
# -e . -> This must be there at the end in requirements.txt. This will help in installing the project 
#         source code as a library. THis will create a file named sensor.egg-info which will have info
#         related to author name, mail, requirements version etc.



REQUIREMENTS_FILE_NAME= 'requirements.txt'
REMOVE_E= "-e ."


def get_requirements():
    # TODO: Write a function that reads all the lines from requirements.txt and returns it as a list.
    with open(REQUIREMENTS_FILE_NAME) as requirements_file:

        requirements_list= requirements_file.readlines()
    requirements_list= [i.replace("\n", "") for i in requirements_list]
    if REMOVE_E in requirements_list:
        requirements_list.remove(REMOVE_E)
    return requirements_list


setup(
    name= "sensor",
    version= "0.0.1",
    author= "Venkata satya anirudh Rani",
    author_email= "anirudhrvs@gmail.com",
    packages= find_packages(),
    install_requires= get_requirements(),

)