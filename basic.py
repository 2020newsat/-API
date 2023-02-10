import win32com.client
import pythoncom
import datetime
from pandas import Series, DataFrame

import sys

sys.path.append("./function")

from tr import *
from etc import *

# ----------------------------------------------------------------------------
# parameter
# ----------------------------------------------------------------------------

opymd = 'W3    '
# 월물은 '202303' / 위클리는 'W1    ' (총 6글자, 만기주 위클 없으니 'W1    ' 다음은  'W3    ')

# id, passwd, acn, pwd
maxQty = 2

# ----------------------------------------------------------------------------
# login
# ----------------------------------------------------------------------------
login(id, passwd, cert_passwd)
today = datetime.datetime.today()
ymd = today.strftime("%Y%m")

order = DataFrame()

balance = T0441(acn, pwd)

if len(balance.index) > 0:
    balance['qty'] = balance['qty'].astype(int)
    order = ClearBalance(balance, maxQty, order)
    order['qty'] = order['qty'].astype(int)
    print('clear order:', order)

op = T2301(opymd)
kp200 = T1511(101)
atm = atm(kp200, op)

# ----------------------------------------------------------------------------
# Strategy
# ----------------------------------------------------------------------------



# ----------------------------------------------------------------------------
# RunOrder: tmCode - bid ask - enter
# ----------------------------------------------------------------------------
print("order ready: ", order)

for row in range(len(order)):
    code = order.iloc[row, 0]
    qty = order.iloc[row, 1]
    strike = CodeToStrike(code)
    BidAsk = T2105(code)  # bid/ask 매수/매도 3호가까지 확인

    if qty > 0:
        bns = '2'
        price = BidAsk['ask3']

    if qty < 0:
        bns = '1'
        qty = - qty
        price = BidAsk['bid3']

    if qty != 0:
        for OrdCount in range(qty):
            print("OrdCount is", OrdCount, code, bns, price)
            OrdNo = CFOAT00100(code, bns, '00', price, 1, acn, passwd)
            #print(OrdNo)

# CFOAT00100(code, BnS, kind, price, qty) - return: OrdNo
# BnS '1' 매도 '2' 매수
# kind '00' 지정가 / '03' 시장가
