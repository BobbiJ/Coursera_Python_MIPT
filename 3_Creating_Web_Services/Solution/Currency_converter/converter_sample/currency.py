from bs4 import BeautifulSoup
from decimal import Decimal
import requests


def convert(amount, cur_from, cur_to, date, requests):
    url = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req='
    response = requests.get(url+date)  # Использовать переданный requests
    soap = BeautifulSoup(response.content, 'lxml')
    #print(soap.prettify())
    if cur_from != 'RUR':
        value_1 = Decimal((soap.find('charcode', text=cur_from).find_next_sibling('value').string).replace(',', '.'))
        nominal_1 = Decimal((soap.find('charcode', text=cur_from).find_next_sibling('nominal').string).replace(',' ,'.'))
        value_2 = Decimal((soap.find('charcode', text=cur_to).find_next_sibling('value').string).replace(',', '.'))
        nominal_2 = Decimal((soap.find('charcode', text=cur_to).find_next_sibling('nominal').string).replace(',', '.'))
        m_1 = value_1/nominal_1
        m_2 = value_2/nominal_2
        res = m_1*amount/m_2
        result = round(res, 4)
    else:
        value_2 = Decimal((soap.find('charcode', text=cur_to).find_next_sibling('value').string).replace(',', '.'))
        nominal_2 = Decimal((soap.find('charcode', text=cur_to).find_next_sibling('nominal').string).replace(',', '.'))
        m_2 = value_2 / nominal_2
        res = amount / m_2
        result = round(res, 4)
    return result  # не забыть про округление до 4х знаков после запятой



if __name__ == '__main__':
    print(convert(1,'RUR','EUR','02/03/2002',requests))