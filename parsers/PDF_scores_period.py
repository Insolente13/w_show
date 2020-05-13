# coding utf-8
import PyPDF2
import os

# pdfFileObj = open('D:\\Счета Билайн pdf\\Eko\\2017\\Билайн Счета август\\386494648.Pdf', 'rb')
dict_1 = {'Счёт-фактура №': ['Договор', 'Дата', 'Сумма без НДС']}

txt_log_x = input('Куда положить на рабочем столе?')
txt_log = open('C:\\Users\\v.martynov\\Desktop\\{0}.txt'.format(txt_log_x), 'w')


# Достаём необходимые данные из PDF преобразуя в txt
def dict_add(pdf_file):
    global dict_1
    global txt_log

    try:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        num_page = pdf_reader.numPages
        find_text = None
        ban_num = None

        for page in range(num_page):

            pars2 = pdf_reader.getPage(page).extractText().encode('cp1252').decode('cp1251')
            if int(page / 50) == float(page / 50):
                print('Мы на странице {0}'.format(page))
            # print('Мы на странице {0}'.format(x))
            # print(pars2)

            if pars2.find('Договор № ') >= 0 or pars2.find('Лицевой счет') >= 0:

                if pars2.find('Договор № ') >= 0:
                    find_text = 'Договор № '
                elif pars2.find('Лицевой счет') >= 0:
                    find_text = 'Лицевой счет'

                ban_numx = pars2.find(find_text) + len(find_text)
                ban_numy = ban_numx + 9
                ban_num = pars2[ban_numx:ban_numy]

                ban_notify = '\nДоговор найден: {0}. На странице {1}'.format(ban_num, page + 1)
                print(ban_notify)
                txt_log.write(ban_notify)

            if pars2.find('СЧЕТ-ФАКТУРА  №') >= 0:
                # print(pars2)
                find_text = 'СЧЕТ-ФАКТУРА  №'
                score_numx = pars2.find(find_text) + len(find_text)
                score_numy = score_numx + 12
                score_num = pars2[score_numx:score_numy]

                score_notify = '\nНомер счёта найден: {0}. На странице {1}'.format(score_num, page + 1)
                print(score_notify)
                txt_log.write(score_notify)
                # print(ban_num)

                dict_1[score_num] = [ban_num, str(), float()]
                # print('Мы на странице {0}'.format(x))
                # print(dict_1, ' 4')
                # print(score_numy)

                find_text2 = 'от'
                find_text3 = '(1а)'

                date_numx = pars2.find(find_text2) + len(find_text2)
                date_numy = pars2.find(find_text3)

                score_date = pars2[date_numx:date_numy]
                dict_1[score_num][1] = score_date

                date_notify = '\nДата счёта найдена: {0}. На странице {1}'.format(score_date, page + 1)
                print(date_notify)
                txt_log.write(date_notify)

                if pars2.find('Услуги связи/Информационные услуги') >= 0 or pars2.find('Услуги связи') >= 0:

                    if pars2.find('Услуги связи/Информационные услуги') >= 0:
                        find_text = 'Услуги связи/Информационные услуги'
                    elif pars2.find('Услуги связи') >= 0:
                        find_text = 'Услуги связи'

                    fst_num = pars2.find(find_text) + len(find_text)
                    find_text3 = '362мес'
                    sec_num = pars2.find(find_text3)
                    score_sum = float(pars2[fst_num:sec_num].replace(',', '.'))
                    dict_1[score_num][2] = score_sum

                    sum_score_notify = '\nСумма счёта найдена: {0}. + НДС {2} На странице {1}'. \
                        format(score_sum, page + 1, round(score_sum * 0.18, 2))
                    print(sum_score_notify)
                    txt_log.write(sum_score_notify)
                    # print(dict_1, ' 5')
                    break

        print('---------------------------------------------')
        return dict_1
    except KeyboardInterrupt:
        print('Ошибка на странице {0}'.format(page))

    txt_log.close()


# Откуда взять файлы
direct = input(r'Введине название пути к папке с файлами')

all_files = os.listdir(direct)
y = 0
count_bans = all_files.count()

# Обход файлов в цикле
for x in all_files:
    y += 1
    print('Мы на {0} бане из {1}'.format(y, count_bans))
    direct_name = direct + '\\' + x
    pdf_file_obj = open(direct_name, 'rb')

    dict_add(pdf_file_obj)

txt_log.close()

# txt_log_dict = open('C:\\Users\\v.martynov\\Desktop\\pdf_to_excel2018.txt', 'w')
txt_log_dict_x = input('Куда логировать на рабочем столе?')
txt_log_dict = open('C:\\Users\\v.martynov\\Desktop\\{0}.txt'.format(txt_log_dict_x), 'w')

for x in dict_1:
    to_write = '\n{0}: {1}'.format(x, dict_1[x])
    txt_log_dict.write(to_write)

txt_log_dict.close()

print('Отработано, {0} файлов!'.format(y))
