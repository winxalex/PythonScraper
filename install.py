__author__ = 'xxx'

import subprocess
import sys

def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])


# Example
if __name__ == '__main__':
    install("py_expression_eval")
    install("pyowm")
    install("pandas")
    install("selenium")
    install("beautifulsoup4")