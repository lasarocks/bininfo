import random
import string
import re
import base64
from app.utils.utils import str2int

def luhn(ccn):
    c = [int(x) for x in ccn[::-2]] 
    u2 = [(2*int(y))//10+(2*int(y))%10 for y in ccn[-2::-2]]
    return sum(c+u2)%10 == 0





def find_X_positions(cc):
    matchs = []
    try:
        for item in re.finditer(r'X+', cc):
            matchs.append(item)
    except Exception as err:
        print(f'find_X_positions exp --- {err}')
    return matchs



def gen_mnX(cc, ocu=None, tentativas=0):
    if tentativas > 300:
        print(f'gen_mnX tentativas > 300 --- quitting')
        return False
    ocu = find_X_positions(cc) if ocu is None else ocu
    if ocu:
        new = ''
        last_pos = 0
        for match in ocu:
            pos_match_start = match.start()
            pos_match_end = match.end()
            found = cc[pos_match_start:pos_match_end]
            if pos_match_start > last_pos:
                new += cc[last_pos:pos_match_start]
                last_pos = pos_match_end
            random_start_from = int('1'.zfill(len(found))[::-1])
            random_end_on = int(''.join('9' for _ in range(0, len(found))))
            new += str(random.randint(random_start_from, random_end_on))
        if last_pos < len(cc):
            new += cc[last_pos:]
        if luhn(new):
            return new
        else:
            return gen_mnX(cc=cc, ocu=ocu, tentativas=tentativas+1)
    return False






def gen_X_on_missing_cc_numbers(base):
    total_digits = 16
    if base.startswith('3'):
        total_digits = 15
    total_missing = total_digits - len(base)
    return f"{base}{''.join('X' for x in range(0, total_missing))}"



def gen_gg_from_bin(cc_bin, qtd=10):
    new_cc_X = gen_X_on_missing_cc_numbers(cc_bin)
    ccs_made = []
    ccs_out = []
    for index in range(0, qtd):
        t_cc = gen_mnX(cc=new_cc_X)
        if t_cc not in ccs_made:
            ccs_made.append(t_cc)
            month = str(random.randint(1, 12)).zfill(2)
            year = random.randint(2025, 2032)
            cvv = str(random.randint(1, 999)).zfill(3)
            ccs_out.append(f'{t_cc}|{month}|{year}|{cvv}')
    return ccs_out



def gen_gg_from_cc_raw(cc_raw, qtd=10):
    cc_data = fmt_cc(cc_raw)
    if not cc_data:
        return False
    ccs_made = []
    ccs_out = []
    for index in range(0, qtd):
        cc_num = cc_data.get("cc").upper()
        if 'X' in cc_num:
            cc_num = gen_mnX(cc_num)
        cc_month = cc_data.get("month").upper()
        if 'X' in cc_month:
            cc_month = str(random.randint(1, 12)).zfill(2)
        cc_year = cc_data.get("year").upper()
        if 'X' in cc_year:
            cc_year = random.randint(2025, 2032)
        cc_cvv = cc_data.get("cvv").upper()
        if 'X' in cc_cvv:
            cc_cvv = str(random.randint(1, 999)).zfill(3)
        temp_new_cc = f'{cc_num}|{cc_month}|{cc_year}|{cc_cvv}'
        if temp_new_cc not in ccs_out:
            ccs_out.append(temp_new_cc)
    return ccs_out







def gen_missing_cc_numbers(base):
    total_missing = 16 - len(base)
    start_from = int('1'.zfill(total_missing)[::-1])
    end_on = int(''.join('9' for _ in range(0, total_missing)))
    return f'{base}{str(random.randint(start_from,end_on))}'


def gen_gg(base, qtd=10):
    out = []
    for i in range(0, qtd):
        temp = gen_missing_cc_numbers(base=base)
        contador = 0
        while luhn(temp) is not True and contador < 100:
            temp = gen_missing_cc_numbers(base=base)
            contador += 1
        if luhn(temp):
            month = str(random.randint(1, 12)).zfill(2)
            year = random.randint(2025, 2032)
            cvv = str(random.randint(1, 999)).zfill(3)
            temp_cc = f'{temp}|{month}|{year}|{cvv}'
            if temp_cc not in out:
                if qtd == 1:
                    return temp_cc
                out.append(temp_cc)
    return out




def fmt_cc(cc_string, printable=False):
    cc_string = cc_string.upper()
    temp_cc = re.findall(r'[0-9X]+', cc_string)
    if len(temp_cc) >= 4:
        cc_splited = {}
        has_find_cc_number = False
        has_find_month = False
        has_find_year = False
        has_find_cvv = False
        for index in range(0, len(temp_cc)):
            cc_item = temp_cc[index]
            if has_find_cc_number is False:
                if len(cc_item) in (15, 16):
                    if cc_item[0] in ('2', '3', '4', '5', '6'):
                        has_find_cc_number = True
                        cc_splited.update(
                            {
                                'cc': cc_item
                            }
                        )
                    else:
                        print(f'invalid initial char {cc_item} -- expecting 2,3,4,5,6')
                        break
                else:
                    print(f'len cc_item not in 15,16 --- {len(cc_item)} -- {cc_item}')
            elif has_find_month is False:
                if len(cc_item) == 2:
                    if cc_item != 'XX':
                        temp_month = str2int(cc_item)
                        if temp_month:
                            if temp_month > 0 and temp_month < 13:
                                cc_item = str(temp_month).zfill(2)
                            else:
                                print(f'invalid month value (lower 0 or bigger 13) -- {cc_item}')
                                break
                        else:
                            print(f'invalid month -- failed convert {cc_item} to int')
                            break
                    has_find_month = True
                    cc_splited.update(
                        {
                            'month': cc_item
                        }
                    )
                else:
                    print(f'invalid month len --- {cc_item}')
                    break
            elif has_find_year is False:
                if len(cc_item) in (2, 4):
                    if 'X' not in cc_item:
                        temp_year = str2int(cc_item)
                        if temp_year:
                            if len(cc_item) == 2:
                                temp_year += 2000
                            if temp_year > 2023 and temp_year < 2050:
                                cc_item = str(temp_year)
                            else:
                                print(f'invalid year value (lower 2023 or bigger 2050) -- {cc_item}')
                                break
                        else:
                            print(f'invalid year -- failed convert {cc_item} to int')
                            break
                    else:
                        if len(cc_item) == 2:
                            cc_item = f'20{cc_item}'
                    has_find_year = True
                    cc_splited.update(
                        {
                            'year': cc_item
                        }
                    )
                else:
                    print(f'invalid year len --- {cc_item}')
                    break
            elif has_find_cvv is False:
                if len(cc_item) in (3, 4):
                    if 'X' not in cc_item:
                        temp_cvv = str2int(cc_item)
                        if not temp_cvv:
                            print(f'invalid cvv -- failed convert {cc_item} to int')
                            break
                    has_find_cvv = True
                    cc_splited.update(
                        {
                            'cvv': cc_item
                        }
                    )
                else:
                    print(f'invalid cvv len --- {cc_item}')
                    break
        if printable is True:
            return '|'.join([x for x in cc_splited.values()])
        return cc_splited
    return False








def formatar_cc(msg, printable=False): 
    temp = re.findall(r'\d+', msg)
    if len(temp) >= 4:
        cc_num = temp[0].strip()
        if luhn(cc_num):
            mes = temp[1].zfill(2)
            ano = temp[2] if len(temp[2]) == 2 else temp[2][2:] if len(temp[2]) == 4 else '30'
            validade = f'{mes}/{ano}'
            cvv = temp[3].strip()
            if printable is True:
                return f'{cc_num}|{mes}|{ano}|{cvv}'
            return {
                'cc': cc_num,
                'month': mes,
                'year': ano,
                'cvv': cvv
            }
    return {}
