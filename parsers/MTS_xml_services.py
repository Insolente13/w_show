import os

import pandas as pd
from lxml import objectify

direct = input('Введине название пути к папке с файлами')


def xml_parser(direct):
    all_file = os.listdir(direct)
    print(all_file)
    my_services = []

    for files in all_file:

        xml = objectify.parse(open(direct + '\\' + files, 'rb'))
        root = xml.getroot()

        try:
            for line in root.tp:
                num = {'number': line.attrib['n']}
                try:
                    for i in line.ss:
                        x = dict(i.attrib)
                        x.update(num)
                        my_services.append(x)
                except AttributeError:
                    print(i, num)
        except AttributeError:
            print('Wow')

        return my_services


services = xml_parser(direct, )

to_w = direct + '\\parse_result_202004.xlsx'
writer = pd.ExcelWriter(to_w, engine='openpyxl')
table = pd.DataFrame(services)
table.to_excel(writer, index=False)
writer.save()
