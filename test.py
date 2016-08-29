import os
import zipfile as zip

cur_path = os.getcwd()
cur_path = "{0}\\dload1".format(cur_path)

if os.path.exists(cur_path):
    print("exists!")
else:
    os.mkdir(cur_path)
