import fdb


class G:
    con = fdb.connect(dsn='baza/Baza.fdb', user='SYSDBA', password='masterkey')  # standard firebird password
    cur = con.cursor()

    
def get_table_headers(table):  # returns all table headers (column names)
    INSERT = "select rdb$field_name from rdb$relation_fields where rdb$relation_name='"+table+"';"  # select all column names from table
    G.cur.execute(INSERT)
    INSERT_temp = G.cur.fetchall()
    INSERT_col = []
    total_columns = len(INSERT_temp)
    for i in range(total_columns):
        temp_result = INSERT_temp[i][0].strip()  # remove white spaces
        INSERT_col += [temp_result]
    G.con.commit()
    return INSERT_col


def get_row_values(table, key):  # returns all values from table with specified key (primary)
    INSERT = "select * from "+table+" where id_formatki='"+key+"'"
    G.cur.execute(INSERT)
    INSERT_temp = G.cur.fetchone()
    total_columns = len(INSERT_temp)
    INSERT_val = []
    for i in range(total_columns):
        temp_result = str(INSERT_temp[i]) if INSERT_temp[i] is not None else ''  # remove white spaces
        INSERT_val += [temp_result]
    G.con.commit()
    return INSERT_val

INSERT_TABLE = 'formatki'
get_columns = get_table_headers('FORMATKI')

element = {
    'prim_key': '18',
    'opis': 'BN1-000',
    'dlugosc': '2000',
    'szerokosc': '500',
    'grubosc': '20',
    'symbol': 'BN1 - polka 000',
    'cecha': 'REG 000',
    'grupa': 'REG 000',
    'id_plyty': 'OJ26125200401P3R1281'
}

data = {
    get_columns[0]: '0',  # BRUTTO2
    get_columns[1]: '0',  # BRUTTO1
    get_columns[2]: '0',  # BRUTTOD
    get_columns[3]: '0',  # NETTO2
    get_columns[4]: '0',  # NETTO1
    get_columns[5]: '0',  # NETTOD
    get_columns[6]: '0',  # VAT
    get_columns[7]: '0',  # BRUTTO
    get_columns[8]: '0',  # NETTO
    get_columns[9]: '0',  # NETTO_SYM
    get_columns[10]: element['opis'],  # OPIS
    get_columns[11]: element['dlugosc'],  # DLUGOSC
    get_columns[12]: element['szerokosc'],  # SZEROKOSC
    get_columns[13]: element['grubosc'],  # GRUBOSC
    get_columns[14]: 'wg zamowienia',  # OPIS_OKLEINY_4
    get_columns[15]: 'wg zamowienia',  # OPIS_OKLEINY_3
    get_columns[16]: 'wg zamowienia',  # OPIS_OKLEINY_2
    get_columns[17]: 'wg zamowienia',  # OPIS_OKLEINY_1
    get_columns[18]: ' ',  # ID_OKLEINY_4
    get_columns[19]: ' ',  # ID_OKLEINY_3
    get_columns[20]: ' ',  # ID_OKLEINY_2
    get_columns[21]: ' ',  # ID_OKLEINY_1
    get_columns[22]: '0',  # MAGAZYN
    get_columns[23]: '0',  # STAN
    get_columns[24]: '0',  # STAN_MIN
    get_columns[25]: '0',  # STAN_MAX
    get_columns[26]: '0',  # PRIORYTET
    get_columns[27]: '0',  #
    get_columns[28]: '1',  # TYP_FORMATKI
    get_columns[29]: ' ',  # ZP_SUB_SUFIX
    get_columns[30]: ' ',  # ID_F_ZESTAWU
    get_columns[31]: 'RYS_PARAM',  # RYS_PARAM
    get_columns[32]: element['prim_key'],  # ID_FORMATKI ->  PRIMARY KEY!
    get_columns[33]: '',  # ID_GRUPY
    get_columns[34]: element['id_plyty'],  # ID_PLYTY
    get_columns[35]: 'ID_RYS',  # ID_RYS
    get_columns[36]: '00000',  # KOD
    get_columns[37]: 'ADMIN-2002.07.01 13:33:37',  # INFO_MOD
    get_columns[38]: 'ADMIN-2002.07.01 13:33:37',  # INFO_DOD
    get_columns[39]: 'ABCD1234',  # RYS_TECH_1
    get_columns[40]: 'NNNN',  # OKLEJANIE
    get_columns[41]: '0',  # SREDNIA_WAZONA
    get_columns[42]: ' ',  # WALUTA
    get_columns[43]: '0',  # ZW
    get_columns[44]: ' ',  # TYP
    get_columns[45]: '0',  # STRUKTURA
    get_columns[46]: '0',  # KOLEJNOSC_OKLEJANIA
    get_columns[47]: element['grupa'],  # GRUPA
    get_columns[48]: element['symbol'],  # SYMBOL
    get_columns[49]: ' ',  # SKLADNIKI
    get_columns[50]: element['cecha'],  # CECHA
    get_columns[51]: '0',  # STRUKTURA_TYP
    get_columns[52]: ' ',  # DRILLCODE
    get_columns[53]: ' ',  # DRILLCODE2
    get_columns[54]: '0',  # NETTO_DOPLATA_LAKIER
    get_columns[55]: ' ',  # CECHA_1
    get_columns[56]: ' ',  # PRODUKCJA_SCIEZKA
    get_columns[57]: '',  # OPIS_ALIAS
    get_columns[58]: ' ',  # DLUGOSC_FORMULA
    get_columns[59]: ' ',  # SZEROKOSC_FORMULA
    get_columns[60]: ' ',  # ILOSC_FORMULA
    get_columns[61]: ' ',  # CNC_PLIK_SZABLON
    get_columns[62]: '',  # DRILLBARCODE
    get_columns[63]: '',  # DRILLINFO
    get_columns[64]: '',  # DRILLBARCODE2
    get_columns[65]: '',  # DRILLINFO2
    get_columns[66]: '',  # DRILLCODE3
    get_columns[67]: '',  # DRILLBARCODE3
    get_columns[68]: '',  # DRILLINFO3
    get_columns[69]: '',  # DRILLCODE4
    get_columns[70]: '',  # DRILLBARCODE4
    get_columns[71]: '',  # DRILLINFO4
    get_columns[72]: '',  # DRILLCODE5
    get_columns[73]: '',  # DRILLBARCODE5
    get_columns[74]: '',  # DRILLINFO5
    get_columns[75]: '',  # DRILLCODE6
    get_columns[76]: '',  # DRILLBARCODE6
    get_columns[77]: '',  # DRILLINFO6
    get_columns[78]: '0',  # NR_OPAKOWANIA
    get_columns[79]: '0',  # RODZAJ_PAKOWANIA
    get_columns[80]: '0'  # CNC_CZAS_OBROBKI
}


temp_INSERT_col = []
temp_INSERT_val = []

for k, v in data.items():
    temp_INSERT_col += [k]
    temp_INSERT_val += [v]

INSERT_val = ''
INSERT_col = ''
for i in range(len(temp_INSERT_val)):
    if i == len(temp_INSERT_val)-1:
        INSERT_val += "'" + str(temp_INSERT_val[i]) + "'"
        INSERT_col += temp_INSERT_col[i]
    else:
        INSERT_val += "'"+str(temp_INSERT_val[i])+"',"
        INSERT_col += str(temp_INSERT_col[i]) + ", "

INSERT_TABLE = 'formatki'
INSERT = 'insert into ' + INSERT_TABLE+' ('+INSERT_col+') values ('+INSERT_val+')'
G.cur.execute(INSERT)
G.con.commit()
