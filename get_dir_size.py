import os
import datetime
 
 
def get_folder_size(path):
  folder_size = 0
 
  if not os.path.exists(path):
    return folder_size
 
  if os.path.isfile(path):
    folder_size = os.path.getsize(path)
    return folder_size
  try:
    if os.path.isdir(path):
      with os.scandir(path) as directory_lists:
        for directory_list in directory_lists:
          if directory_list.is_dir():
            sub_folder_size = get_folder_size(directory_list.path) # 递归获取大小
            folder_size += sub_folder_size
          elif directory_list.is_file():
            file_size = os.path.getsize(directory_list.path)
            folder_size += file_size
 
        return folder_size
  except:
    pass
 
 
# 以下主要是为了格式化输出
def get_file_length(file_name):
  characters = list(file_name)
  ascii_length = 0
  utf8_length = 0
 
  for character in characters:
    if ord(character) < 128:
      ascii_length += 1
    else:
      utf8_length += 2
 
  return ascii_length + utf8_length
 
 
def main(basedir):
  with os.scandir(basedir) as dirs:
    directory_size = []
    for dir in dirs:
      try:
        if not dir.is_file():
          dirsize = round(get_folder_size(dir.path) / 1000000) # return the file size in Mb
          resformat = [dir.name, dirsize]
          directory_size.append(resformat)
      except:
        pass
    results = sorted(directory_size, key=lambda x: x[1], reverse=True) # return a list ordered by size
    results = [[i[0], '文件夹大小：' + str(i[1]) + ' Mb'] for i in results]

    try:
      with open(basedir + os.sep + datetime.date.today().isoformat() + '.txt', 'a+') as f:
        for result in results:
          # 按照50的宽度格式化输出结果
          len1 = 50 - get_file_length(result[0]) + len(result[0])
          len2 = 25 - get_file_length(result[1]) + len(result[1])
          f.writelines('{:<{len1}s} {:>{len2}s}\n'.format(result[0], result[1], len1=len1, len2=len2))
    except PermissionError:
      print("請輸入臨時保存路徑")

      basedir = input()

      with open(basedir + os.sep + datetime.date.today().isoformat() + '.txt', 'a+') as f:
        for result in results:
          # 按照50的宽度格式化输出结果
          len1 = 50 - get_file_length(result[0]) + len(result[0])
          len2 = 25 - get_file_length(result[1]) + len(result[1])
          f.writelines('{:<{len1}s} {:>{len2}s}\n'.format(result[0], result[1], len1=len1, len2=len2))

      print('The result was successfully saved in the directory with date as file name.')
 
 
if __name__ == "__main__":
  basedir = input("Please input the directory you would like to know the sizes: ")
  main(basedir)