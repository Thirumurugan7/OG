import subprocess
import os
from pymongo import MongoClient


client = MongoClient('mongodb+srv://nagi:nagi@cluster0.ohv5gsc.mongodb.net/nagidb')


db = client['Og3Collection'] 
collection = db['Og3']

def do_line(num=0):
  SIZE = os.get_terminal_size()
  COL = SIZE.columns
  LINE = SIZE.lines
  return "-"*(COL-num) if num!=0 else "-"*(COL)

# JavaScript code to be executed
def upload(js_code, upload_file):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

    temp_js_path = os.path.join(parent_dir, 'temp_script.js')
    with open(temp_js_path, 'w') as temp_js_file:
        temp_js_file.write(js_code)

    try:
        result = subprocess.run(['node', temp_js_path], capture_output=True, text=True)
        print(f"\n \n{do_line()}\nFile Root Hash:",result.stdout, do_line(1))
        print("File Upload error : "+str(result.stderr) if result.stderr else "")
        sample = collection.insert_many([{"result":result, "data": upload_file}])
    finally:
        os.remove(temp_js_path)
