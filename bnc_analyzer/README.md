Install python3 from http://www.python.org
Important installation details:
- On the first wizard screen, check the box "Add python 3.9 to path" 
- On the last creen, if the option is shown, disable Max path width.

Using a "prompt" terminal run the command:

pip install pandas openpyxl xlwt

Copy [bnc_analyzer.py](https://raw.githubusercontent.com/mauriciodev/pdrinex/main/bnc_analyzer/bnc_analyzer.py) (right click, save as...) to the root folder where the .ppp files are. The script creates a XLS file for each .ppp file found on the subfolders.
