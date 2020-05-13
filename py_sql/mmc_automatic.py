import pandas as pd

import Work_moduls.eko_sql as es

run = es.cursor.execute
nums_file = pd.read_excel('C:\\Users\\v.martynov\\Downloads\\ММЦ 13.03.2020.xlsx', index=True)

xlsx_writer = pd.ExcelWriter('C:\\Users\\v.martynov\\Downloads\\ММЦ 13.03.2020_готово.xlsx',
                             engine='xlsxwriter')

nums_file.to_excel(xlsx_writer, 'Номера', index=False)

count_nums = nums_file.count()[0]
val = '('

for ban_count in range(count_nums - 1):
    val = val + str(nums_file['Номера'][ban_count]) + '),('

val = val + str(nums_file['Номера'][count_nums - 1]) + ')'

insert_comand = f'insert into test._m_nums_for_serv (phone) values {val};'

run('''use ekomobile;''')
run('''SET sql_notes = 0;''')

run(f'''drop temporary table if exists test._m_nums_for_serv;''')
run(f'''create temporary table test._m_nums_for_serv (phone bigint(20), primary key(phone));''')


run(insert_comand)

run('''
drop temporary table if exists test._m_serv_fx;
create temporary table test._m_serv_fx
select i_id, bee_sync, fee, fee_type, lump_sum, moboperator from o_service_fx;
alter table test._m_serv_fx add primary key(i_id);

drop temporary table if exists test._m_eko_serv_hst;
create temporary table test._m_eko_serv_hst
select b.phone, 
	a.service_id, 
    c.bee_sync, 
    c.fee, 
    c.fee_type, 
    c.lump_sum,
    a.requested,
    a.activated, 
    a.unrequested,
    a.deactivated,
    c.moboperator
from hstr_service_fx a 
	inner join test._m_nums_for_serv b on a.object_id = b.phone
	inner join test._m_serv_fx c on a.service_id = c.i_id
where a.deactivated is null or a.deactivated >= now();
''')

# снять
run('''select phone, bee_sync from test._m_eko_serv_hst 
	where moboperator in (64, 65, 66, 67, 68) and bee_sync not in ('eko_SILENCE', 'eko_NATSROAM2', 'eko_VSRNEWB', 'eko_MN_RF')
group by phone, bee_sync;
''')

answer = es.cursor.fetchall()
data_f = pd.DataFrame(list(answer), columns=['Номер', 'Услуга'])
data_f.to_excel(xlsx_writer, 'Снять', index=False)

run('''drop temporary table if exists test._m_bee_serv_hst;
create temporary table test._m_bee_serv_hst
select b.phone, 
	a.service_id, 
    c.bee_sync, 
    c.fee, 
    c.fee_type, 
    c.lump_sum,
    a.startDate,
    a.endDate,
    c.moboperator
from beeline_services_report a 
	inner join test._m_nums_for_serv b on a.msisdn = b.phone
	inner join test._m_serv_fx c on a.service_id = c.i_id
where a.endDate is null or a.endDate >= now();
alter table test._m_bee_serv_hst add key (phone), 
	add key (service_id);
''')


run('''
# GPRSNOT_C на отключение. 06.11.2019 Диана А.
drop temporary table if exists test._m_needed_services;
create temporary table test._m_needed_services
select i_id, bee_sync, moboperator from o_service_fx 
	where bee_sync in ('R02SMT_0', 'eko_SILENCE', 'eko_NATSROAM2', 'eko_VSRNEWB', 'eko_MN_RF');
alter table test._m_needed_services add primary key(i_id);

drop temporary table if exists test._m_all_services_needed;
create temporary table test._m_all_services_needed
select a.phone, b.i_id as service_id, b.bee_sync from test._m_nums_for_serv a inner join test._m_needed_services b
	where b.moboperator is null or b.moboperator not in (64, 65, 66, 67, 68);
alter table test._m_all_services_needed add key (phone), 
	add key (service_id), 
    add column in_bee tinyint(5) default 0;

update test._m_all_services_needed a 
	inner join test._m_bee_serv_hst b on a.phone = b.phone and a.service_id = b.service_id
set a.in_bee = 1;
''')

# подключить в Билайне
run('''
select phone, bee_sync from test._m_all_services_needed where in_bee = 0;
''')

answer = es.cursor.fetchall()
data_f = pd.DataFrame(list(answer), columns=['Номер', 'Услуга'])
data_f.to_excel(xlsx_writer, 'Подключить', index=False)

run('''
drop temporary table if exists test._m_all_EKO_services_needed;
create temporary table test._m_all_EKO_services_needed
select a.phone, b.i_id as service_id, b.bee_sync from test._m_nums_for_serv a inner join test._m_needed_services b
	where b.moboperator in (64, 65, 66, 67, 68);
alter table test._m_all_EKO_services_needed add key (phone), 
	add key (service_id), 
    add column in_eko tinyint(5) default 0;

update test._m_all_EKO_services_needed a 
	inner join test._m_eko_serv_hst b on a.phone = b.phone and a.service_id = b.service_id
set a.in_eko = 1;
''')

# такие внести
run('''
select phone, bee_sync from test._m_all_EKO_services_needed where in_eko = 0;
''')
answer = es.cursor.fetchall()
data_f = pd.DataFrame(list(answer), columns=['Номер', 'Услуга'])
data_f.to_excel(xlsx_writer, 'Внести', index=False)

# сменить тариф на PREDPROD
run('''select a.phone from test._m_nums_for_serv a 
inner join o_ctn b on a.phone = b.i_id where b.operator_tarif <> 3500;''')
answer = es.cursor.fetchall()
data_f = pd.DataFrame(list(answer), columns=['Номер'])
data_f.to_excel(xlsx_writer, 'на PREDPROD', index=False)

# МН тарификаторы
run('''drop temporary table if exists test._m_atom_farm_on_nums;
create temporary table test._m_atom_farm_on_nums
select b.phone, a.serviceId from beeline_services_report a 
inner join test._m_nums_for_serv b on a.msisdn = b.phone
where a.service_id in (28, 334, 2748, 3452) and (a.endDate is null or a.endDate >= now()) and a.startDate <= now()
group by b.phone;''')

run('''select phone, serviceId from test._m_atom_farm_on_nums;''')
answer = es.cursor.fetchall()
data_f = pd.DataFrame(list(answer), columns=['Номер', 'Услуга'])
data_f.to_excel(xlsx_writer, 'Отключить МН', index=False)



# отбираем номера, где надо сменить договор
run('''
drop temporary table if exists test._m_nums_on_other_bans;
create temporary table test._m_nums_on_other_bans
select a.phone, c.oan from test._m_nums_for_serv a 
	inner join o_ctn b on a.phone = b.i_id 
    inner join o_operator_agree c on b.operator_agree = c.i_id
    where b.operator_agree not in (49, 408, 175, 405, 21236, 21239, 21238, 21237);
alter table test._m_nums_on_other_bans add column new_ban varchar(256);''')

run('''select phone, oan from test._m_nums_on_other_bans;''')

answer = es.cursor.fetchall()
data_count = pd.DataFrame(list(answer), columns=['Номер', 'Старый договор'])

# Смотрим общее количество номеров на договоре для принятия решения о переносе дс
run('''
drop temporary table if exists test._m_count_nums;
create temporary table test._m_count_nums
select operator_agree, count(*) from o_ctn
    where operator_agree in (49, 408, 175, 405, 21236, 21239, 21238, 21237) group by operator_agree
    order by `count(*)`;
alter table test._m_count_nums add primary key (operator_agree), add column oan varchar(256);

update test._m_count_nums a inner join o_operator_agree b on a.operator_agree = b.i_id
    set a.oan = b.oan;
''')

run('''select oan, `count(*)` from test._m_count_nums;''')

answer = es.cursor.fetchall()
ban_count = pd.DataFrame(list(answer), columns=['ban', 'count'])

ban_count_len = ban_count.shape[0]
data_count_len = data_count.shape[0]

middle_count = int(round(ban_count['count'].sum() / ban_count_len + data_count_len / ban_count_len, 2))


ban_count['Новое количество'] = middle_count - ban_count['count']
ban_count = ban_count[ban_count['Новое количество'] > 0]

range_len = ban_count_len
len_update = data_count_len


# проверяем количество номеров на банах для равномерноего распределения новых
for ban_count in range(range_len):
    if ban_count['Новое количество'][ban_count] > 0 and len_update > 0:

        if len_update > int(ban_count['Новое количество'][ban_count]):

            limit_update = int(ban_count['Новое количество'][ban_count])
            run(f'''update test._m_nums_on_other_bans set new_ban = {ban_count['ban'][ban_count]} limit {limit_update}''')
            len_update -= int(ban_count['Новое количество'][ban_count])
            ban_count['Новое количество'][ban_count] = 0

        elif len_update <= int(ban_count['Новое количество'][ban_count]):
            limit_update = len_update
            run(f'''update test._m_nums_on_other_bans set new_ban = {ban_count['ban'][ban_count]} limit {limit_update}''')
            ban_count['Новое количество'][ban_count] -= limit_update
            len_update = 0

    elif len_update <= 0:
        break

run('''select * from test._m_nums_on_other_bans;''')
answer = es.cursor.fetchall()
ban_change = pd.DataFrame(list(answer), columns=['ban', 'Текущий договор', 'Новый договор'])
ban_change.to_excel(xlsx_writer, 'Сменить договор', index=False)

xlsx_writer.save()
