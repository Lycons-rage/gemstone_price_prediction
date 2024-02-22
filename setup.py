from setuptools import find_packages, setup
from typing import List



HYPHEN_E_DOT = '-e .'

def get_requirements(file_path:str) -> List[str]:
    requirements = ""
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()   # will read line by line from requirements.txt file
        requirements = [req.replace("\n","") for req in requirements]  # when line changes it will encounter a \n and we have to replace it with blank character
        
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)      # -e . will trigger this setup.py file but we need to remove it as it is unwanted character while installing
        
    return requirements




setup(
    name = 'RegressorProject',
    version = '0.0.1',
    author= 'Chinmaya Tewari',
    author_email= 'chinmayatewari.20@gmail.com',
    install_requires = get_requirements('requirements.txt'),
    packages = find_packages()
)