
def up(file,file_data):
   with open(file, "wb") as f:
      f.write(file_data)
      f.close()