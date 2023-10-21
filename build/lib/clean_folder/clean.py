import re
import sys
from pathlib import Path
import shutil


CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = dict()

for cyrillic, latin in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(cyrillic)] = latin
    TRANS[ord(cyrillic.upper())] = latin.upper()

def normilize(name):
    translate_name = re.sub(r'W', '_', name.translate(TRANS))
    return translate_name




JPEG_IMAGES = []
JPG_IMAGES = []
PNG_IMAGES = []
SVG_IMAGES = []
AVI_VIDEO = []
MP4_VIDEO = []
MOV_VIDEO = []
MKV_VIDEO = []
DOC_DOCUM = []
DOCX_DOCUM = []
TXT_DOCUM = []
PDF_DOCUM = []
XLSX_DOCUM = []
PPTX_DOCUM = []
MP3_AUDIO = []
OGG_AUDIO = []
WAV_AUDIO = []
AMR_AUDIO = []
ARCHIVES_ZIP = []
ARCHIVES_GZ = []
ARCHIVES_TAR = []
MY_OTHER = []



REGISTER_EXTENSION = {
    "JPEG": JPEG_IMAGES,
    'JPG': JPG_IMAGES,
    'PNG': PNG_IMAGES,
    'SVG': SVG_IMAGES,
    'AVI': AVI_VIDEO,
    'MP4': MP4_VIDEO,
    'MOV': MOV_VIDEO,
    'MKV': MKV_VIDEO,
    'DOC': DOC_DOCUM,
    'DOCX': DOCX_DOCUM,
    'TXT': TXT_DOCUM,
    'PDF': PDF_DOCUM,
    'XLSX': XLSX_DOCUM,
    'PPTX': PPTX_DOCUM,
    'MP3': MP3_AUDIO,
    'OGG': OGG_AUDIO,
    'WAV': WAV_AUDIO,
    'AMR': AMR_AUDIO,
    'ZIP': ARCHIVES_ZIP,
    'GZ': ARCHIVES_GZ,
    'TAR': ARCHIVES_TAR,
}

FOLDERS = []
EXTENSIONS = set()
UNKNOWN = set()

def get_extension(name: str) -> str:
    return Path(name).suffix[1:].upper()

def scan(folder: Path):
    for item in folder.iterdir():
        #работа с папкой
        if item.is_dir(): #проверяем есть ли объект папка
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'MY_OTHER'):
                FOLDERS.append(item)
                scan(item)
            continue

        #Работа с файлом

        extension = get_extension(item.name) #берем расширение
        full_name = folder / item.name # берем полный путь к файлу
        if not extension:
            MY_OTHER.append(full_name)
        else:
            try:                                     #проверяем расширения, если его нет в словаре то добавляем в неизвестные и другие
                ext_reg =  REGISTER_EXTENSION[extension]
                ext_reg.append(full_name)  #расфасовали по списку
                EXTENSIONS.add(extension) #добавили неизвестные скрипту расширения
            except KeyError:
                UNKNOWN.add(extension)
                MY_OTHER.append(full_name)




def handle_media(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)  # создаем папку
    new_file_name = target_folder / (normilize(file_name.stem) + file_name.suffix)
    file_name.replace(new_file_name)

def handle_audio(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)  # создаем папку
    new_file_name = target_folder / (normilize(file_name.stem) + file_name.suffix)
    file_name.replace(new_file_name)

def handle_video(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)  # создаем папку
    new_file_name = target_folder / (normilize(file_name.stem) + file_name.suffix)
    file_name.replace(new_file_name)

def handle_documents(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)  # создаем папку
    new_file_name = target_folder / (normilize(file_name.stem) + file_name.suffix)
    file_name.replace(new_file_name)

def handle_archive(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)  # создаем папку
    folder_for_file = target_folder / normilize(file_name.stem)
    folder_for_file.mkdir(exist_ok=True)
    try:
        shutil.unpack_archive(str(file_name.absolute()), str(folder_for_file.absolute()))
    except shutil.ReadError:
        folder_for_file.rmdir()
        return
    file_name.unlink()

def handle_folder(folder: Path):
    try:
        folder.rmdir
    except OSError:
        print('Error during remove folder {folder}')

   
def main(folder: Path):
    scan(folder)
    for file in JPEG_IMAGES:
        handle_media(file, folder / 'images' / 'JPEG')
    for file in JPG_IMAGES:
        handle_media(file, folder / 'images' / 'JPG') 
    for file in PNG_IMAGES:
        handle_media(file, folder / 'images' / 'PNG')
    for file in SVG_IMAGES:
        handle_media(file, folder / 'images' / 'SVG')

    for file in AVI_VIDEO:
        handle_video(file, folder / 'video' / 'AVI')
    for file in MP4_VIDEO:
        handle_video(file, folder / 'video' / 'MP4')
    for file in MOV_VIDEO:
        handle_video(file, folder / 'video' / 'MOV')
    for file in MKV_VIDEO:
        handle_video(file, folder / 'video' / 'MKV')

    for file in DOC_DOCUM:
        handle_documents(file, folder / 'documents' / 'DOC')
    for file in DOCX_DOCUM:
        handle_documents(file, folder / 'documents' / 'DOCX')
    for file in TXT_DOCUM:
        handle_documents(file, folder / 'documents' / 'TXT')
    for file in PDF_DOCUM:
        handle_documents(file, folder / 'documents' / 'PDF')
    for file in XLSX_DOCUM:
        handle_documents(file, folder / 'documents' / 'XLSX')
    for file in PPTX_DOCUM:
        handle_documents(file, folder / 'documents' / 'PPTX')

    for file in MP3_AUDIO:
        handle_audio(file, folder / 'audio' / 'MP3')
    for file in OGG_AUDIO:
        handle_audio(file, folder / 'audio' / 'OGG')
    for file in WAV_AUDIO:
        handle_audio(file, folder / 'audio' / 'WAV')
    for file in AMR_AUDIO:
        handle_audio(file, folder / 'audio' / 'AMR')
        
    for file in ARCHIVES_ZIP:
        handle_archive(file, folder / 'archives' / 'ZIP')
    for file in ARCHIVES_GZ:
        handle_archive(file, folder / 'archives' / 'GZ')
    for file in ARCHIVES_TAR:
        handle_archive(file, folder / 'archives' / 'TAR')
    
    for file in MY_OTHER:
        handle_media(file, folder / 'MY_OTHER')



    for folder in FOLDERS[::-1]:     #удаляем пустые папки после сортировки
        try:
            folder.name.replace(folder.name, normilize(folder.name))
            folder.rmdir()
        except OSError:
            print('Error during remove folder {folder}')  


def start():
    if sys.argv[1]:
        folder_process = Path(sys.argv[1])
        main(folder_process)


