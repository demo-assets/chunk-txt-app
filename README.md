# chunk-txt-app
This repo contains a python application that chunks TXT files. It will do an auto discovery of text encoding which allows you to read different OS text encoding types.

# Steps to configure
- Open the script.
- Scroll to the bottom and specify the text file path that you need to chunk.
- Below it you specify the path that you want to output the json docs to

# Steps to run
I recommend running everyting in a python virtual environment to avoid messing any system libraries: 
- python3 -m venv myenv (for Mac M1) or python -m venv myenv
- source myenv/bin/activate
- pip install chardet
- python file-name.py
