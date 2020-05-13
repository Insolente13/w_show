# coding utf-8
import PyPDF2
import os


# Парсер PDF
def copy_charges(pdf_file_obj):
    # global to_paste
    # global x
    pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)
    count_pages = pdf_reader.numPages

    x_break = 0

    for page in range(0, count_pages):
        pars2 = pdf_reader.getPage(page). \
            extractText().encode('cp1252').decode('cp1251')

        if x_break == 2:
            print('Вышли из файла Брейком на странице {0}!'.format(page))
            break
        else:
            if pars2.find('Операции') >= 0 \
                    or pars2.find('Разовые начисления(руб.)') >= 0:
                dog = 'Договор'
                page_num = 'Лист'

                page_place = pars2.find(page_num)
                first_dog = pars2.find(dog)
                pars2_1 = pars2[first_dog + len(dog):page_place]
                sec_dog = pars2_1.find(dog)
                pars2_2 = pars2_1[sec_dog + len(dog):].replace('   ', '\n')
                list_of_charges = pars2_2.split('\n')

                for hhh in list_of_charges:
                    # print(hhh[1:] + '\t' + x + '\n')
                    to_paste.write(hhh[1:] + '\t' + x + '\n')
                    if hhh.find('Итог') >= 0:
                        x_break += 1


# Откуда взять
direct = input(r'Введине название пути к папке с файлами')
all_files = os.listdir(direct)
count_bans = all_files.count()

# Куда положить
fileNum = input('Введите номер файла для записи начислений!')
fileNumDirect = 'D:\\charges' + fileNum + '.txt'
to_paste = open(fileNumDirect, 'a')

y = 0

# обходим файлы в цикле
for x in all_files:
    y += 1
    print('Мы на {0} файле из {1}'.format(y, count_bans))
    direct_name = direct + '\\' + x
    pdf_file = open(direct_name, 'rb')
    copy_charges(pdf_file)

to_paste.close()

print('Отработано, {0} файлов!'.format(y))
