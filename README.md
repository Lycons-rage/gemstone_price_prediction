## END TO END ML PROJECT

### CREATE AND ACTIVATE THE ENVIRONMENT
```
conda create -p venv python==version_number_here

conda activate venv/
```
### INSTALL THE REQUIREMENTS
```
pip install -r requirements.txt
```

#### HOW WE SETUP THE PROJECT:
- After creating and activating the environment, we create a requirements.txt file, inside which are all the required libraries and modules for the project. This document ends with "-e .", which is used to trigger another file setup.py
- We create a folder with name src, containing all the program files of our project, including _init__.py, logger and exception handler
- When setup.py is triggered python installs all the required libraries, if not found
- Moreover, a seperate directory is created containing all the information regarding project version and file structure