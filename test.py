import win32com.client
import pythoncom
import datetime
from pandas import Series, DataFrame

import sys

sys.path.append("/PycharmProjects/XingApi (32bit)/function")

from tr import *
from CFOAT00100 import *
from etc import *
from OneStopOrder import *
from OrderForParameter import *
from t2105 import *
from Strategy import *


opymd = 'W3    '
# 월물은 '202303' / 위클리는 'W1    ' (총 6글자, 만기주 위클 없으니 'W1    ' 다음은  'W3    ')
id = 
passwd =
cert_passwd = "공인인증서 비번"
acn =   # 계좌번호
pwd =   # 계좌비번

login(id, passwd, cert_passwd)
today = datetime.datetime.today()
ymd = today.strftime("%Y%m")

balance = T0441(acn, pwd)
balance['qty'] = balance['qty'].astype(int)
print(balance)

order = DataFrame()
order = ClearBalance(balance, order)
order['qty'] = order['qty'].astype(int)
print(order)

op = T2301(opymd)
kp200 = T1511(101)
atm = atm(kp200, op)
print(atm)

