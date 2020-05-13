import logging

from Work_moduls import eko_sql
from api.BeeApiMethod import as_proxies, bee_api_auth

# запуск sql запросов
run = eko_sql.cursor.execute

# логгирование
logger = logging.getLogger('api')
logger.setLevel(level=logging.DEBUG)

log_path = 'api.log'

fh = logging.FileHandler(log_path, encoding='utf8')
fh.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

# Достаём список логинов и паролей
run('''select a.oan, c.login, c.password from o_operator_agree a 
	inner join o_subdivision b on a.subdivision = b.i_id 
	inner join o_account_info c on a.i_id = c.operator_agree
where b.brand = 2 and c.access_type = 1''')

account_info = eko_sql.cursor.fetchall()
acc_dict = {account_info[a][0]: (account_info[a][1], account_info[a][2]) for a in range(len(account_info))}

print('Запрашиваем токены по всем банам, в количестве ' + str(len(acc_dict)))

# получаем token, если нет, то в лог
for oan, data in acc_dict.items():
    try:
        bee_api_auth(data[0], data[1], proxies=as_proxies)
        # log.debug(f'{oan}, token получен!')
    except Exception as exc:
        logger.debug(f'{oan}, {exc.args}')
