#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 18-9-30
@Author  : leemiracle
汇率数据
"""


import time
import datetime
from collections import defaultdict
import requests
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(levelname)1.1s %(name)s: %(message)s', filename="/tmp/exchange_list.log")
logger = logging.getLogger(__name__)



COUNTRY2CURRENCY = {
    'AE': {'currency': 'AED', 'name': 'United Arab Emirates'},
    'AF': {'currency': 'AFN', 'name': 'Afghanistan'},
    'AL': {'currency': 'ALL', 'name': 'Albania'},
    'AM': {'currency': 'AMD', 'name': 'Armenia'},
    'CW': {'currency': 'ANG', 'name': 'Curaçao'},
    'SX': {'currency': 'ANG', 'name': 'Sint Maarten (Dutch part)'},
    'AO': {'currency': 'AOA', 'name': 'Angola'},
    'AR': {'currency': 'ARS', 'name': 'Argentina'},
    'AU': {'currency': 'AUD', 'name': 'Australia'},
    'AW': {'currency': 'AWG', 'name': 'Aruba'},
    'AZ': {'currency': 'AZN', 'name': 'Azerbaijan'},
    'BA': {'currency': 'BAM', 'name': 'Bosnia and Herzegovina'},
    'BB': {'currency': 'BBD', 'name': 'Barbados'},
    'BD': {'currency': 'BDT', 'name': 'Bangladesh'},
    'BG': {'currency': 'BGN', 'name': 'Bulgaria'},
    'BH': {'currency': 'BHD', 'name': 'Bahrain'},
    'BI': {'currency': 'BIF', 'name': 'Burundi'},
    'BM': {'currency': 'BMD', 'name': 'Bermuda'},
    'BN': {'currency': 'BND', 'name': 'Brunei Darussalam'},
    'BO': {'currency': 'BOB', 'name': 'Bolivia (Plurinational State of)'},
    'BR': {'currency': 'BRL', 'name': 'Brazil'},
    'BS': {'currency': 'BSD', 'name': 'Bahamas'},
    'BT': {'currency': 'BTN', 'name': 'Bhutan'},
    'BW': {'currency': 'BWP', 'name': 'Botswana'},
    'BY': {'currency': 'BYN', 'name': 'Belarus'},
    'BZ': {'currency': 'BZD', 'name': 'Belize'},
    'CA': {'currency': 'CAD', 'name': 'Canada'},
    'CD': {'currency': 'CDF', 'name': 'Congo (Democratic Republic of the)'},
    'CH': {'currency': 'CHF', 'name': 'Switzerland'},
    'CL': {'currency': 'CLP', 'name': 'Chile'},
    'CN': {'currency': 'CNY', 'name': 'China'},
    'CO': {'currency': 'COP', 'name': 'Colombia'},
    'CR': {'currency': 'CRC', 'name': 'Costa Rica'},
    'CV': {'currency': 'CVE', 'name': 'Cabo Verde'},
    'CZ': {'currency': 'CZK', 'name': 'Czech Republic'},
    'DJ': {'currency': 'DJF', 'name': 'Djibouti'},
    'DK': {'currency': 'DKK', 'name': 'Denmark'},
    'DO': {'currency': 'DOP', 'name': 'Dominican Republic'},
    'DZ': {'currency': 'DZD', 'name': 'Algeria'},
    'EG': {'currency': 'EGP', 'name': 'Egypt'},
    'ER': {'currency': 'ERN', 'name': 'Eritrea'},
    'ET': {'currency': 'ETB', 'name': 'Ethiopia'},
    'LU': {'currency': 'EUR', 'name': 'Luxembourg'},
    'MT': {'currency': 'EUR', 'name': 'Malta'},
    'CY': {'currency': 'EUR', 'name': 'Cyprus'},
    'DE': {'currency': 'EUR', 'name': 'Germany'},
    'EE': {'currency': 'EUR', 'name': 'Estonia'},
    'AT': {'currency': 'EUR', 'name': 'Austria'},
    'SK': {'currency': 'EUR', 'name': 'Slovakia'},
    'FR': {'currency': 'EUR', 'name': 'France'},
    'BE': {'currency': 'EUR', 'name': 'Belgium'},
    'LT': {'currency': 'EUR', 'name': 'Lithuania'},
    'LV': {'currency': 'EUR', 'name': 'Latvia'},
    'ES': {'currency': 'EUR', 'name': 'Spain'},
    'NL': {'currency': 'EUR', 'name': 'Netherlands'},
    'IT': {'currency': 'EUR', 'name': 'Italy'},
    'SI': {'currency': 'EUR', 'name': 'Slovenia'},
    'PT': {'currency': 'EUR', 'name': 'Portugal'},
    'IE': {'currency': 'EUR', 'name': 'Ireland'},
    'FI': {'currency': 'EUR', 'name': 'Finland'},
    'GR': {'currency': 'EUR', 'name': 'Greece'},
    'FJ': {'currency': 'FJD', 'name': 'Fiji'},
    'FK': {'currency': 'FKP', 'name': 'Falkland Islands (Malvinas)'},
    'GB': {'currency': 'GBP', 'name': 'United Kingdom'},
    'GE': {'currency': 'GEL', 'name': 'Georgia'},
    'GH': {'currency': 'GHS', 'name': 'Ghana'},
    'GI': {'currency': 'GIP', 'name': 'Gibraltar'},
    'GM': {'currency': 'GMD', 'name': 'Gambia'},
    'GN': {'currency': 'GNF', 'name': 'Guinea'},
    'GT': {'currency': 'GTQ', 'name': 'Guatemala'},
    'GY': {'currency': 'GYD', 'name': 'Guyana'},
    'HK': {'currency': 'HKD', 'name': 'Hong Kong'},
    'HN': {'currency': 'USD', 'name': 'Honduras'},
    'HR': {'currency': 'HRK', 'name': 'Croatia'},
    'HT': {'currency': 'HTG', 'name': 'Haiti'},
    'HU': {'currency': 'HUF', 'name': 'Hungary'},
    'ID': {'currency': 'IDR', 'name': 'Indonesia'},
    'IL': {'currency': 'ILS', 'name': 'Israel'},
    'IN': {'currency': 'INR', 'name': 'India'},
    'IQ': {'currency': 'IQD', 'name': 'Iraq'},
    'IR': {'currency': 'IRR', 'name': 'Iran (Islamic Republic of)'},
    'IS': {'currency': 'ISK', 'name': 'Iceland'},
    'JM': {'currency': 'JMD', 'name': 'Jamaica'},
    'JO': {'currency': 'JOD', 'name': 'Jordan'},
    'JP': {'currency': 'JPY', 'name': 'Japan'},
    'KE': {'currency': 'KES', 'name': 'Kenya'},
    'KG': {'currency': 'KGS', 'name': 'Kyrgyzstan'},
    'KH': {'currency': 'KHR', 'name': 'Cambodia'},
    'KM': {'currency': 'KMF', 'name': 'Comoros'},
    'KP': {'currency': 'KPW', 'name': "Korea (Democratic People's Republic of)"},
    'KR': {'currency': 'KRW', 'name': 'Korea, Republic Of Republic Of Korea'},
    'KW': {'currency': 'KWD', 'name': 'Kuwait'},
    'KY': {'currency': 'KYD', 'name': 'Cayman Islands'},
    'KZ': {'currency': 'KZT', 'name': 'Kazakhstan'},
    'LA': {'currency': 'LAK', 'name': "Lao People's Democratic Republic"},
    'LB': {'currency': 'LBP', 'name': 'Lebanon'},
    'LK': {'currency': 'LKR', 'name': 'Sri Lanka'},
    'LR': {'currency': 'LRD', 'name': 'Liberia'},
    'LS': {'currency': 'LSL', 'name': 'Lesotho'},
    'LY': {'currency': 'LYD', 'name': 'Libya'},
    'MA': {'currency': 'MAD', 'name': 'Morocco'},
    'MD': {'currency': 'MDL', 'name': 'Moldova (Republic of)'},
    'MG': {'currency': 'MGA', 'name': 'Madagascar'},
    'MK': {'currency': 'MKD', 'name': 'Macedonia (the former Yugoslav Republic of)'},
    'MM': {'currency': 'MMK', 'name': 'Myanmar'},
    'MN': {'currency': 'MNT', 'name': 'Mongolia'},
    'MO': {'currency': 'MOP', 'name': 'Macao'},
    'MR': {'currency': 'MRO', 'name': 'Mauritania'},
    'MU': {'currency': 'MUR', 'name': 'Mauritius'},
    'MV': {'currency': 'MVR', 'name': 'Maldives'},
    'MW': {'currency': 'MWK', 'name': 'Malawi'},
    'MX': {'currency': 'MXN', 'name': 'Mexico'},
    'MY': {'currency': 'MYR', 'name': 'Malaysia'},
    'MZ': {'currency': 'MZN', 'name': 'Mozambique'},
    'NA': {'currency': 'NAD', 'name': 'Namibia'},
    'NG': {'currency': 'NGN', 'name': 'Nigeria'},
    'NI': {'currency': 'NIO', 'name': 'Nicaragua'},
    'NO': {'currency': 'NOK', 'name': 'Norway'},
    'NP': {'currency': 'NPR', 'name': 'Nepal'},
    'NZ': {'currency': 'NZD', 'name': 'New Zealand'},
    'OM': {'currency': 'OMR', 'name': 'Oman'},
    'PA': {'currency': 'PAB', 'name': 'Panama'},
    'PE': {'currency': 'PEN', 'name': 'Peru'},
    'PG': {'currency': 'PGK', 'name': 'Papua New Guinea'},
    'PH': {'currency': 'PHP', 'name': 'Philippines'},
    'PK': {'currency': 'PKR', 'name': 'Pakistan'},
    'PL': {'currency': 'PLN', 'name': 'Poland'},
    'PY': {'currency': 'PYG', 'name': 'Paraguay'},
    'QA': {'currency': 'QAR', 'name': 'Qatar'},
    'RO': {'currency': 'RON', 'name': 'Romania'},
    'RS': {'currency': 'RSD', 'name': 'Serbia'},
    'RU': {'currency': 'RUB', 'name': 'Russia'},
    'RW': {'currency': 'RWF', 'name': 'Rwanda'},
    'SA': {'currency': 'SAR', 'name': 'Saudi Arabia'},
    'SB': {'currency': 'SBD', 'name': 'Solomon Islands'},
    'SC': {'currency': 'SCR', 'name': 'Seychelles'},
    'SD': {'currency': 'SDG', 'name': 'Sudan'},
    'SE': {'currency': 'SEK', 'name': 'Sweden'},
    'SG': {'currency': 'SGD', 'name': 'Singapore'},
    'SH': {'currency': 'SHP', 'name': 'Saint Helena, Ascension and Tristan da Cunha'},
    'SL': {'currency': 'SLL', 'name': 'Sierra Leone'},
    'SO': {'currency': 'SOS', 'name': 'Somalia'},
    'SR': {'currency': 'SRD', 'name': 'Suriname'},
    # 'SS': {'currency': 'SSP', 'name': 'South Sudan'},
    'ST': {'currency': 'STD', 'name': 'Sao Tome and Principe'},
    'SY': {'currency': 'SYP', 'name': 'Syrian Arab Republic'},
    'SZ': {'currency': 'SZL', 'name': 'Swaziland'},
    'TH': {'currency': 'THB', 'name': 'Thailand'},
    'TJ': {'currency': 'TJS', 'name': 'Tajikistan'},
    'TM': {'currency': 'TMT', 'name': 'Turkmenistan'},
    'TN': {'currency': 'TND', 'name': 'Tunisia'},
    'TO': {'currency': 'TOP', 'name': 'Tonga'},
    'TR': {'currency': 'TRY', 'name': 'Turkey'},
    'TT': {'currency': 'TTD', 'name': 'Trinidad and Tobago'},
    'TW': {'currency': 'TWD', 'name': 'Taiwan'},
    'TZ': {'currency': 'TZS', 'name': 'Tanzania, United Republic Of'},
    'UA': {'currency': 'UAH', 'name': 'Ukraine'},
    'UG': {'currency': 'UGX', 'name': 'Uganda'},
    'US': {'currency': 'USD', 'name': 'United States'},
    'UY': {'currency': 'UYU', 'name': 'Uruguay'},
    'UZ': {'currency': 'UZS', 'name': 'Uzbekistan'},
    'VE': {'currency': 'VES', 'name': 'Venezuela (Bolivarian Republic of)'},
    'VN': {'currency': 'VND', 'name': 'Vietnam'},
    'VU': {'currency': 'VUV', 'name': 'Vanuatu'},
    'WS': {'currency': 'WST', 'name': 'Samoa'},
    'YE': {'currency': 'YER', 'name': 'Yemen'},
    'ZA': {'currency': 'ZAR', 'name': 'South Africa'},
    'ZM': {'currency': 'ZMW', 'name': 'Zambia'},
    'SV': {'currency': 'USD', 'name': 'El Salvador'},
    'EC': {'currency': 'USD', 'name': 'Ecuador'},

}

currency_list = list(set(v['currency'] for v in COUNTRY2CURRENCY.values()))

standard_currency = 'USD'


def isAvaliableFloat(value):
    flag = False
    try:
        value = float(value)
        if value > 0:
            flag = True
    except ValueError:
        pass
    return flag


def crawl_currency():
    utc_date_time = datetime.datetime.utcnow()
    date_time = utc_date_time + datetime.timedelta(hours=8) + datetime.timedelta(days=5)
    timestamp = int(time.mktime(date_time.timetuple()) * 1000)
    print(utc_date_time, timestamp, type(date_time))
    currencies = [("fx_s" + c + standard_currency).lower() for c in currency_list]
    logger.info('http://hq.sinajs.cn/?rn={timestamp}&list={currency_list}'.format(timestamp=timestamp,
                                                                            currency_list=",".join(currencies)))
    rep = requests.get('http://hq.sinajs.cn/?rn={timestamp}&list={currency_list}'.format(timestamp=timestamp,
                                                                                         currency_list=",".join(
                                                                                             currencies)))
    print('http://hq.sinajs.cn/?rn={timestamp}&list={currency_list}'.format(timestamp=timestamp,
                                                                                         currency_list=",".join(
                                                                                             currencies)))
    dic = defaultdict(dict)
    try:
        for item in rep.text.split("\n"):
            if item:
                info = item.partition('var hq_str_fx_s')[2]
                info = info.replace('"', '').replace(";", "")
                detail = info.partition('=')
                currency_name = detail[0].partition('usd')[0] if detail[0] != "usdusd" else "usd"
                item_info_list = detail[2].split(",")
                # print(info)
                if len(item_info_list) > 2:
                    value = 0.0
                    for d in item_info_list:
                        if d and isAvaliableFloat(d):
                            value = float(d)
                            break
                    dic[currency_name] = {
                        # "time": item_info_list[0],
                        "to_usd": value,
                        "datetime": item_info_list[-1] + " " + item_info_list[0],
                    }
    except Exception as e:
        logger.info(str(e))
        # traceback.print_exc(e)
    # print(len(dic.keys()))
    # print(dic)
    return dic


def update_history_data(start='2018-1-1', end='2018-8-29', single_code_list=None):
    'https://www.oanda.com/fx-for-business/historical-rates/api/data/update/?&source=OANDA&adjustment=0&base_currency=USD&start_date=2018-8-4&end_date=2018-9-3&period=daily&price=bid&view=graph&quote_currency_0=EUR&quote_currency_1=BGN&quote_currency_2=&quote_currency_3=&quote_currency_4=&quote_currency_5=&quote_currency_6=&quote_currency_7=&quote_currency_8=&quote_currency_9='
    base_currency = 'USD'
    # quote_currency_0 = 'BGN'
    base_uri = 'https://www.oanda.com/fx-for-business/historical-rates/api/data/update/?&source=OANDA&adjustment=0&base_currency={base_currency}&start_date={start}&end_date={end}&period=daily&price=bid&view=graph&quote_currency_0={quote_currency_0}&quote_currency_1=&quote_currency_2=&quote_currency_3=&quote_currency_4=&quote_currency_5=&quote_currency_6=&quote_currency_7=&quote_currency_8=&quote_currency_9='
    dic = defaultdict(dict)
    global currency_list
    if single_code_list:
        single_code_list = [s for s in single_code_list]
        currency_list = single_code_list
    for q in currency_list:
        print(q, start, end)
        uri = base_uri.format(base_currency=q, start=start, end=end, quote_currency_0=base_currency) # 换美元
        rep = requests.get(uri)
        data = rep.json()
        time.sleep(1)
        info_list = data['widget'][0]['data']
        for d in info_list:
            date_time = d[0]
            price = float(d[1])
            q = q.lower()
            dic[date_time].update({q: {"to_usd": price}})
    print(dic)
    # dic = {1535846400000: {'pkr': {'to_usd': 123.517109}, 'tzs': {'to_usd': 2282.2}, 'ron': {'to_usd': 3.991723}, 'myr': {'to_usd': 4.109679}, 'inr': {'to_usd': 70.68}, 'jpy': {'to_usd': 111.049468}, 'czk': {'to_usd': 22.175389}, 'brl': {'to_usd': 4.054284}, 'sar': {'to_usd': 3.745739}, 'zar': {'to_usd': 14.66149}, 'sgd': {'to_usd': 1.371145}, 'usd': {'to_usd': 1.0}, 'aud': {'to_usd': 1.389814}, 'chf': {'to_usd': 0.968334}, 'qar': {'to_usd': 3.640358}, 'sek': {'to_usd': 9.124019}, 'ngn': {'to_usd': 361.524275}, 'cny': {'to_usd': 6.830096}, 'pen': {'to_usd': 3.301651}, 'hrk': {'to_usd': 6.406895}, 'clp': {'to_usd': 681.082241}, 'aed': {'to_usd': 3.672693}, 'huf': {'to_usd': 280.98702}, 'vnd': {'to_usd': 23290.5}, 'kzt': {'to_usd': 363.38}, 'nok': {'to_usd': 8.366246}, 'rub': {'to_usd': 67.482565}, 'mxn': {'to_usd': 19.058144}, 'pln': {'to_usd': 3.700974}, 'php': {'to_usd': 53.536368}, 'hkd': {'to_usd': 7.848466}, 'cop': {'to_usd': 3057.320772}, 'twd': {'to_usd': 30.670838}, 'egp': {'to_usd': 17.805776}, 'idr': {'to_usd': 14721.295366}, 'bgn': {'to_usd': 1.685396}, 'thb': {'to_usd': 32.631506}, 'try': {'to_usd': 6.522964}, 'ils': {'to_usd': 3.604067}, 'gbp': {'to_usd': 0.771605}, 'nzd': {'to_usd': 1.5102}, 'eur': {'to_usd': 0.861729}, 'dkk': {'to_usd': 6.422878}, 'cad': {'to_usd': 1.303692}}, 1535760000000: {'pkr': {'to_usd': 123.545}, 'tzs': {'to_usd': 2282.2}, 'ron': {'to_usd': 3.9934}, 'myr': {'to_usd': 4.10925}, 'inr': {'to_usd': 70.68}, 'jpy': {'to_usd': 111.041}, 'czk': {'to_usd': 22.17585}, 'brl': {'to_usd': 4.0538}, 'sar': {'to_usd': 3.74555}, 'zar': {'to_usd': 14.65703}, 'sgd': {'to_usd': 1.37107}, 'usd': {'to_usd': 1.0}, 'aud': {'to_usd': 1.389661}, 'chf': {'to_usd': 0.96819}, 'qar': {'to_usd': 3.6404}, 'sek': {'to_usd': 9.12095}, 'ngn': {'to_usd': 361.5}, 'cny': {'to_usd': 6.82985}, 'pen': {'to_usd': 3.3016}, 'hrk': {'to_usd': 6.4066}, 'clp': {'to_usd': 681.075}, 'aed': {'to_usd': 3.6727}, 'huf': {'to_usd': 280.962}, 'vnd': {'to_usd': 23290.5}, 'kzt': {'to_usd': 363.38}, 'nok': {'to_usd': 8.3636}, 'rub': {'to_usd': 67.47015}, 'mxn': {'to_usd': 19.05435}, 'pln': {'to_usd': 3.70089}, 'php': {'to_usd': 53.545}, 'hkd': {'to_usd': 7.84842}, 'cop': {'to_usd': 3057.1}, 'twd': {'to_usd': 30.671}, 'egp': {'to_usd': 17.8052}, 'idr': {'to_usd': 14725.0}, 'bgn': {'to_usd': 1.685276}, 'thb': {'to_usd': 32.622}, 'try': {'to_usd': 6.51764}, 'ils': {'to_usd': 3.60445}, 'gbp': {'to_usd': 0.771313}, 'nzd': {'to_usd': 1.509981}, 'eur': {'to_usd': 0.861668}, 'dkk': {'to_usd': 6.42237}, 'cad': {'to_usd': 1.30334}}, 1535587200000: {'pkr': {'to_usd': 123.114161}, 'tzs': {'to_usd': 2278.113059}, 'ron': {'to_usd': 3.966561}, 'myr': {'to_usd': 4.112604}, 'inr': {'to_usd': 70.802003}, 'jpy': {'to_usd': 111.388577}, 'czk': {'to_usd': 22.038228}, 'brl': {'to_usd': 4.132019}, 'sar': {'to_usd': 3.748934}, 'zar': {'to_usd': 14.579342}, 'sgd': {'to_usd': 1.366376}, 'usd': {'to_usd': 1.0}, 'aud': {'to_usd': 1.37335}, 'chf': {'to_usd': 0.970103}, 'qar': {'to_usd': 3.619327}, 'sek': {'to_usd': 9.125862}, 'ngn': {'to_usd': 360.926914}, 'cny': {'to_usd': 6.833725}, 'pen': {'to_usd': 3.284575}, 'hrk': {'to_usd': 6.363464}, 'clp': {'to_usd': 672.086414}, 'aed': {'to_usd': 3.672495}, 'huf': {'to_usd': 279.295511}, 'vnd': {'to_usd': 23184.762598}, 'kzt': {'to_usd': 362.611284}, 'nok': {'to_usd': 8.335418}, 'rub': {'to_usd': 68.108187}, 'mxn': {'to_usd': 19.052619}, 'pln': {'to_usd': 3.673621}, 'php': {'to_usd': 53.474813}, 'hkd': {'to_usd': 7.848841}, 'cop': {'to_usd': 3011.378579}, 'twd': {'to_usd': 30.693395}, 'egp': {'to_usd': 17.84698}, 'idr': {'to_usd': 14747.510547}, 'bgn': {'to_usd': 1.674213}, 'thb': {'to_usd': 32.686001}, 'try': {'to_usd': 6.61216}, 'ils': {'to_usd': 3.609048}, 'gbp': {'to_usd': 0.768183}, 'nzd': {'to_usd': 1.502021}, 'eur': {'to_usd': 0.856011}, 'dkk': {'to_usd': 6.382582}, 'cad': {'to_usd': 1.295029}}, 1535500800000: {'pkr': {'to_usd': 122.871612}, 'tzs': {'to_usd': 2279.458408}, 'ron': {'to_usd': 3.962706}, 'myr': {'to_usd': 4.112699}, 'inr': {'to_usd': 70.451248}, 'jpy': {'to_usd': 111.418837}, 'czk': {'to_usd': 22.00664}, 'brl': {'to_usd': 4.128675}, 'sar': {'to_usd': 3.748634}, 'zar': {'to_usd': 14.328685}, 'sgd': {'to_usd': 1.365244}, 'usd': {'to_usd': 1.0}, 'aud': {'to_usd': 1.367546}, 'chf': {'to_usd': 0.97432}, 'qar': {'to_usd': 3.621707}, 'sek': {'to_usd': 9.14863}, 'ngn': {'to_usd': 361.320828}, 'cny': {'to_usd': 6.817535}, 'pen': {'to_usd': 3.281612}, 'hrk': {'to_usd': 6.356889}, 'clp': {'to_usd': 664.530771}, 'aed': {'to_usd': 3.672534}, 'huf': {'to_usd': 277.871099}, 'vnd': {'to_usd': 23203.56398}, 'kzt': {'to_usd': 362.459443}, 'nok': {'to_usd': 8.346202}, 'rub': {'to_usd': 67.978826}, 'mxn': {'to_usd': 19.038278}, 'pln': {'to_usd': 3.661266}, 'php': {'to_usd': 53.390118}, 'hkd': {'to_usd': 7.848889}, 'cop': {'to_usd': 2987.515628}, 'twd': {'to_usd': 30.68402}, 'egp': {'to_usd': 17.873656}, 'idr': {'to_usd': 14661.674123}, 'bgn': {'to_usd': 1.673194}, 'thb': {'to_usd': 32.645467}, 'try': {'to_usd': 6.379045}, 'ils': {'to_usd': 3.622085}, 'gbp': {'to_usd': 0.773303}, 'nzd': {'to_usd': 1.490863}, 'eur': {'to_usd': 0.85549}, 'dkk': {'to_usd': 6.379041}, 'cad': {'to_usd': 1.292288}}, 1535673600000: {'pkr': {'to_usd': 123.264971}, 'tzs': {'to_usd': 2280.379889}, 'ron': {'to_usd': 3.983058}, 'myr': {'to_usd': 4.111079}, 'inr': {'to_usd': 70.838299}, 'jpy': {'to_usd': 110.929204}, 'czk': {'to_usd': 22.121476}, 'brl': {'to_usd': 4.122189}, 'sar': {'to_usd': 3.748645}, 'zar': {'to_usd': 14.691997}, 'sgd': {'to_usd': 1.369903}, 'usd': {'to_usd': 1.0}, 'aud': {'to_usd': 1.384273}, 'chf': {'to_usd': 0.968139}, 'qar': {'to_usd': 3.599939}, 'sek': {'to_usd': 9.123223}, 'ngn': {'to_usd': 361.61348}, 'cny': {'to_usd': 6.831668}, 'pen': {'to_usd': 3.291989}, 'hrk': {'to_usd': 6.384792}, 'clp': {'to_usd': 679.748241}, 'aed': {'to_usd': 3.672553}, 'huf': {'to_usd': 280.394979}, 'vnd': {'to_usd': 23246.455289}, 'kzt': {'to_usd': 363.219262}, 'nok': {'to_usd': 8.352507}, 'rub': {'to_usd': 67.815326}, 'mxn': {'to_usd': 19.119977}, 'pln': {'to_usd': 3.689563}, 'php': {'to_usd': 53.496948}, 'hkd': {'to_usd': 7.848671}, 'cop': {'to_usd': 3041.790409}, 'twd': {'to_usd': 30.691753}, 'egp': {'to_usd': 17.802375}, 'idr': {'to_usd': 14786.012708}, 'bgn': {'to_usd': 1.680013}, 'thb': {'to_usd': 32.701063}, 'try': {'to_usd': 6.600111}, 'ils': {'to_usd': 3.604181}, 'gbp': {'to_usd': 0.769831}, 'nzd': {'to_usd': 1.507363}, 'eur': {'to_usd': 0.858977}, 'dkk': {'to_usd': 6.403558}, 'cad': {'to_usd': 1.30284}}}
    data_sorted = sorted([{k: dic[k]}for k in dic.keys()], key=lambda x: x.keys()[0])
    for da in data_sorted:
        date_time = da.keys()[0]
        for ke in COUNTRY2CURRENCY.keys():
            currency_code = COUNTRY2CURRENCY[ke]['currency']
            if currency_code not in currency_list:
                continue
            currency_code = currency_code.lower()
            d = dict(
                currency_code=currency_code,
                country_name=COUNTRY2CURRENCY[ke]['name'],
                sina_update_time=datetime.datetime.fromtimestamp(0),
                currency_date=datetime.datetime.fromtimestamp(date_time/1000),
                to_usd=da[date_time][currency_code]['to_usd'],
                country_code=ke
            )
            print(d)


def main():
    logger.info("start crawl")
    dic = crawl_currency()
    currency_date = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    logger.info("{} dic length:{}".format(currency_date, len(dic.keys())))
    for i, k in enumerate(COUNTRY2CURRENCY.keys()):
        currency_code = COUNTRY2CURRENCY[k]['currency']
        currency_code = currency_code.lower()
        # logger.info(currency_code, dic[currency_code])
        d = dict(
            currency_code=currency_code,
            country_name = COUNTRY2CURRENCY[k]['name'],
            sina_update_time=dic[currency_code]['datetime'],
            to_usd=dic[currency_code]['to_usd'],
            country_code=k,
            currency_date=currency_date
        )
        # update_currency(d)
        print("{}:{}".format(i, k))


if __name__ == '__main__':
    update_history_data()
    main()
