import win32com.client
import pythoncom
import datetime
from pandas import Series, DataFrame

import sys

sys.path.append("./function")

from tr import *
from etc import *


# ----------------------------------------------------------------------------
# login
# ----------------------------------------------------------------------------

class XASessionEventHandler:
    login_state = 0

    def OnLogin(self, code, msg):
        if code == "0000":
            XASessionEventHandler.login_state = 1
        else:
            print("로그인 실패")


def login(id, passwd, cert_passwd):
    instXASession = win32com.client.DispatchWithEvents("XA_Session.XASession", XASessionEventHandler)
    instXASession.ConnectServer("demo.ebestsec.co.kr", 20001)
    # 접속할 서버의 기본 주소는 'hts.ebestsec.co.kr'
    # 모의 투자인 경우에는 'demo.ebestsec.co.kr'

    instXASession.Login(id, passwd, cert_passwd, 0, 0)

    while XASessionEventHandler.login_state == 0:
        pythoncom.PumpWaitingMessages()

    return


# ----------------------------------------------------------------------------
# atm finder
# ----------------------------------------------------------------------------
def atm(kp200, op):
    nearKp200 = int(kp200 * 0.4) / 0.4

    NearOp = DataFrame()
    NearOp = op[op.index >= nearKp200 - 10]
    NearOp = NearOp[NearOp.index <= nearKp200 + 10]
    minCP = min(NearOp['LenCP'])
    atm = NearOp.loc[NearOp['LenCP'] == minCP].index
    return atm


# ----------------------------------------------------------------------------
# CodeToStrike 종목코드로 행사가, 콜풋 여부 찾기
# ----------------------------------------------------------------------------

# 0  201T2330  매수  1.0
# 1  201T2332  매도  1.0
# 2  301T2317  매도  1.0
# 3  301T2320  매수  1.0

def CodeToStrike(code):
    strike = float(code[5:])
    if strike % 5 > 0:
        strike = strike + 0.5
    return strike


# ----------------------------------------------------------------------------
# StriketoCode: 옵션 행사가, 코드 반환 함수
# ----------------------------------------------------------------------------
def StrikeToCode(strike, op, cp):
    cCode = op.loc[strike, 'cCode'].iloc[0]
    pCode = op.loc[strike, 'pCode'].iloc[0]
    if cp == 'c':
        code = cCode
    elif cp == 'p':
        code = pCode
    return code


# ----------------------------------------------------------------------------
# SetOrder: 주문 미리 받아두고 한 번에 실행
# ----------------------------------------------------------------------------
def SetOrder(code, qty, bns, order):
    if bns == 'b':
        qty = qty
    if bns == 's':
        qty = -qty

    print("order set:", order)
    for row in range(len(order)):
        if order.iloc[row, 0] == code and len(order) > 0:
            print("old order: ", order)
            print("code - qty: ", code, qty)
            order.iloc[row, 1] += qty
            print("new order: ", order)
            # code for deleting order
            # if order.iloc[row, 1] == 0:
            # print("QTY == 0, len: ", len(order))
            #  if len(order) > 1:
            #    print("drop row: ", row)
            #  order = order.drop(row)
            # else:
            #  order = order.drop(order.index[-1])

            # print("modified ", qty, order)
            return order

    new_row = {'code': code, 'qty': qty}
    # print("new", new_row)
    order = order.append(new_row, ignore_index=True)
    return order


# ----------------------------------------------------------------------------
# ClearBalance: 잔고청산
# ----------------------------------------------------------------------------
def ClearBalance(balance, maxQty, order):
    for i in range(len(balance)):
        code = balance.iloc[i, 0]
        qty = balance.iloc[i, 2]
        strike = CodeToStrike(code)

        if balance.iloc[i, 1] == '매수':
            bns = 's'
        if balance.iloc[i, 1] == '매도':
            bns = 'b'

        order = SetOrder(code, qty, bns, order)
    return order


def Straddle(tm, atm, op, maxQty, order):
    order = SetOrderTM(tm, atm, 'c', 's', op, maxQty, order)
    order = SetOrderTM(tm, atm, 'p', 's', op, maxQty, order)
    return order


def SetOrderTM(tm, atm, cp, bns, op, maxQty, order):
    if cp == 'c':
        strike = atm + tm * 2.5
        code = StrikeToCode(strike, op, 'c')
    if cp == 'p':
        strike = atm - tm * 2.5
        code = StrikeToCode(strike, op, 'p')
    order = SetOrder(code, maxQty, bns, order)
    return order
