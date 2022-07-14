import pathlib
import shutil
import sys


TRANS = {
        1072: 'a', 1040: 'A', 1073: 'b', 1041: 'B', 1074: 'v', 1042: 'V', 1075: 'g', 1043: 'G', 1076: 'd', 1044: 'D',
        1077: 'e', 1045: 'E', 1105: 'e', 1025: 'E', 1078: 'j', 1046: 'J', 1079: 'z', 1047: 'Z', 1080: 'i', 1048: 'I',
        1081: 'j', 1049: 'J', 1082: 'k', 1050: 'K', 1083: 'l', 1051: 'L', 1084: 'm', 1052: 'M', 1085: 'n', 1053: 'N',
        1086: 'o', 1054: 'O', 1087: 'p', 1055: 'P', 1088: 'r', 1056: 'R', 1089: 's', 1057: 'S', 1090: 't', 1058: 'T',
        1091: 'u', 1059: 'U', 1092: 'f', 1060: 'F', 1093: 'h', 1061: 'H', 1094: 'ts', 1062: 'TS', 1095: 'ch', 1063: 'CH',
        1096: 'sh', 1064: 'SH', 1097: 'sch', 1065: 'SCH', 1098: '', 1066: '', 1099: 'y', 1067: 'Y', 1100: '', 1068: '',
        1101: 'e', 1069: 'E', 1102: 'yu', 1070: 'YU', 1103: 'ya', 1071: 'YA', 1108: 'je', 1028: 'JE', 1110: 'i', 1030: 'I',
        1111: 'ji', 1031: 'JI', 1169: 'g', 1168: 'G'
        }


def main():

    """
    the main function
    """
    dir_list, file_list = [], []


    if len(sys.argv) < 2:
        user_path = ""
    else:
        user_path = sys.argv[1]

    path = check_path(user_path)

    dir_list, file_list = iter_files_on_dirs(path, dir_list, file_list)

    file_dict, extension_set = check_file_extension(file_list)  # розділити сет на відомі скрипту файли і невідомі-------------

    create_folders(file_dict,path)

    move_files(file_dict,path)








def check_file_extension(file_list):
    """
    checks the file extension
    creates a dictionary with a set of files divided into groups
    """
    file_dict = {
                    "images":[],
                    "documents":[],
                    "audio":[],
                    "video":[],
                    "archives":[],
                    "others":[],
                }

    extension_types = {
                    "images":['JPEG', 'PNG', 'JPG', 'SVG','BMP', "TIF", "TIFF"],
                    "documents":['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
                    "audio":['MP3', 'OGG', 'WAV', 'AMR'],
                    "video":['AVI', 'MP4', 'MOV', 'MKV'],
                    "archives":['ZIP', 'GZ', 'TAR'],
                    }

    extension_set = set()
    
        
    for file_p in file_list:
        file_s = str(file_p)
        idx_extension = file_s.rfind(".")
        extension = file_s[idx_extension+1:]

        extension_set.add(extension)  # розділити сет на відомі скрипту файли і невідомі-----------------

        if extension.upper() in extension_types["images"]:
            file_dict['images'].append(file_p)
        elif extension.upper() in extension_types["documents"]:
            file_dict["documents"].append(file_p)
        elif extension.upper() in extension_types["audio"]:
            file_dict["audio"].append(file_p)
        elif extension.upper() in extension_types["video"]:
            file_dict["video"].append(file_p)
        elif extension.upper() in extension_types["archives"]:
            file_dict["archives"].append(file_p)
        else:
            file_dict["others"].append(file_p)

    return file_dict, extension_set
        

def check_path(user_path):
    
    """
    checks the path to the file folder
    """
    path = pathlib.Path(user_path)
    if path.exists():
        if path.is_dir():
            return path
        else:
            print(f"{path} is file")
    else:
        print(f"path {path.absolute()} not exists")


def create_folders(file_dict,path): # перевірити чи папки такі не створені там де перебираємо файли

    """
    creates folders to transfer found files according to formats
    """
    
    for category, files in file_dict.items():
        if not file_dict[category]:
            continue
        pathlib.Path(str(path) + "/" + category).mkdir()



def iter_files_on_dirs(path, dir_list, file_list):
    
    """
    the function iterates files and folders through the parent folder
    returns a list of file addresses and a list of folder addresses
    """
    if path.is_dir():

        dir_list.append(path.absolute())
        for element in path.iterdir():
            iter_files_on_dirs(element, dir_list, file_list)
    else:
        file_list.append(path.absolute())
    
    return dir_list, file_list


def move_files(file_dict,path):
    """
    ----------------------------------------
    """

    for category, files_path in file_dict.items():
        
        if category == "archives":
            continue

        for file_path in files_path:
            file_name_full = pathlib.Path(file_path).name
            idx_extension = file_name_full.rfind(".")
            file_name = file_name_full[:idx_extension]
            extension = file_name_full[idx_extension+1:]
            norm_file_name = normalize(file_name)
            dst = pathlib.Path(str(path) + "/" + category + "/" + norm_file_name + "." + extension)

            shutil.move(file_path, dst)



def normalize(file_name):  # якщо ім'я вже було то додати символ в кінці файлу

    """
    returns the normalized filename
    replaces other characters and spaces with an underscore
    replaces all Cyrillic characters with Latin characters
    """

    for char in file_name:
        if not char.isalnum() and char != "_":
            file_name = file_name.replace(char, '_')

    return file_name.translate(TRANS)


if __name__ == "__main__":
    main()

#python sort.py C:\Users\user\Desktop\Rozibraty
#python sort.py C:\Users\user\Desktop\Rozibraty\відео_файл.avi
#python sort.py grfeffde
#python sort.py