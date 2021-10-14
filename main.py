# Задание №1
import zipfile
import os
import hashlib

directory_to_extract_to = 'C:\\Users\\ACER\\Desktop\\lab_1'  # директория извлечения файлов архива
arch_file = 'C:\\Users\\ACER\\Desktop\\tiff-4.2.0_lab1.zip'  # путь к архиву

# Создать новую директорию, в которую будет распакован архив
# С помощью модуля zipfile извлечь содержимое архива в созданную директорию
os.mkdir(directory_to_extract_to)

with zipfile.ZipFile(arch_file, 'r') as zip_file:
    zip_file.extractall(directory_to_extract_to)


# Задание №2.1
# Получить список файлов (полный путь) формата txt, находящихся в directory_to_extract_to. Сохранить полученный список в txt_files
txt_files = []
for r, d, f in os.walk(directory_to_extract_to):
    for file in f:
        if file.endswith(".txt"):
            txt_files.append(os.path.join(r, file))

# Задание №2.2
# Получить значения MD5 хеша для найденных файлов и вывести полученные данные на экран.

for file in txt_files:
    target_file_data = open(file, 'rb').read()
    result = hashlib.md5(target_file_data).hexdigest()
    str1 = "".join(file)
    index = str1.rfind('\\')
    print(str1[index + 1:], '\t', result)

# Задание №3
target_hash = "4636f9ae9fef12ebd56cd39586d33cfb"
target_file = ''  # полный путь к искомому файлу
target_file_data = ''  # содержимое искомого файла

# Найти файл MD5 хеш которого равен target_hash в directory_to_extract_to
for r, d, f in os.walk(directory_to_extract_to):
    for file in f:
        if file.endswith(".sh"):
            target_file = os.path.join(r, file)
            target_file_data = open(target_file, 'rb').read()
            result = hashlib.md5(target_file_data).hexdigest()
            if str(result) == target_hash:
                break

# Отобразить полный путь к искомому файлу и его содержимое на экране
print("\n\n")
print(target_file)
print(target_file_data)


# Задание №4
# Ниже представлен фрагмент кода парсинга HTML страницы с помощью регулярных выражений. Возможно выполнение этого задания иным способом (например, с помощью сторонних модулей).

import requests
import re

r = requests.get(target_file_data)
result_dct = {}  # словарь для записи содержимого таблицы

counter = 0
# Получение списка строк таблицы
lines = re.findall(r'<div class="Table-module_row__3TH83">.*?</div>.*?</div>.*?</div>.*?</div>.*?</div>', r.text)
for line in lines:
    # извлечение заголовков таблицы
    if counter == 0:
        # Удаление тегов
        headers = re.sub(r'\<[^>]*\>', "", line)
        # Извлечение списка заголовков
        headers = re.findall('[А-Я][^А-Я]*', headers)
    else:
        temp = re.sub(r'\<[^>]*\>', ';', line)
        temp = re.sub(r'\([^)]*\)', '', temp)
        # Замена последовательности символов ';' на одиночный символ
        temp = re.sub(r"([;])\1+", r"\1", temp)
        # Удаление символа ';' в начале и в конце строки
        temp = temp.strip(";")
        temp = re.sub(r'^\W+', '', temp)

        # Разбитие строки на подстроки
        tmp_split = temp.split(";")
        # Извлечение и обработка (удаление "лишних" символов) данных из первого столбца
        country_name = tmp_split[0]
        # Извлечение данных из оставшихся столбцов. Данные из этих столбцов должны иметь числовое значение (прочерк можно заменить на -1).
        # Некоторые строки содержат пробелы в виде символа '\xa0'.
        col1_val = tmp_split[1]
        col2_val = tmp_split[2]
        col3_val = tmp_split[3]
        col4_val = tmp_split[4]
        col3_val = col3_val.replace("*", "")

        col4_val = re.sub(r'_', '-1', col4_val)
        col1_val = re.sub(r'\xa0', '', col1_val)
        col2_val = re.sub(r'\xa0', '', col2_val)
        col3_val = re.sub(r'\xa0', '', col3_val)
        col4_val = re.sub(r'\xa0', '', col4_val)
        # Запись извлеченных данных в словарь
        result_dct[country_name] = ([int(col1_val), int(col2_val), int(col3_val), int(col4_val)])
    counter += 1

# Задание №5
# Запись данных из полученного словаря в файл
output = open('data.csv', 'w')
output.write(';')
for i in range(0, 4):
    output.write(headers[i] + ';')
output.write('\n')
for key in result_dct.keys():
    output.write(key)
    for i in range(0, 4):
        output.write(';' + str(result_dct.get(key)[i]))
    output.write('\n')
output.close()

# Задание №6
#Вывод данных на экран для указанного первичного ключа (первый столбец таблицы)
target_country = input("Введите название страны: ")
print(result_dct[target_country])