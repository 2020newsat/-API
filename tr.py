import win32com.client
import pythoncom
import datetime
from pandas import Series, DataFrame

import sys

sys.path.append("C:/Users/박위성/PycharmProjects/XingApi (32bit)/function")

from CFOAT00100 import *
from etc import *
from OneStopOrder import *
from OrderForParameter import *
from t2105 import *
from tr import *



# ----------------------------------------------------------------------------
# T2301 옵션전광판
# ----------------------------------------------------------------------------
class XAQueryEventHandlerT2301:
    query_state = 0

    def OnReceiveData(self, code):
        XAQueryEventHandlerT2301.query_state = 1


def T2301(opymd):
    XAQueryEventHandlerT2301.query_state = 0
    instXAQueryT2301 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEventHandlerT2301)
    instXAQueryT2301.ResFileName = "C:\\eBEST\\xingAPI\\Res\\t2301.res"

    instXAQueryT2301.SetFieldData("t2301InBlock", 'yyyymm', 0, opymd)
    # 미니, 일반은 yyyymm, 위클리는 'W1    '
    instXAQueryT2301.SetFieldData("t2301InBlock", "gubun", 0, 'W')
    # 'W' weekly 'M' 미니 'G' 일반

    instXAQueryT2301.Request(0)
    op = DataFrame()


    while XAQueryEventHandlerT2301.query_state == 0:
        pythoncom.PumpWaitingMessages()

    count = instXAQueryT2301.GetBlockCount("t2301OutBlock1")
    for i in range(count):
        actprice = float(instXAQueryT2301.GetFieldData("t2301OutBlock1", "actprice", i))
        callP = float(instXAQueryT2301.GetFieldData("t2301OutBlock1", "price", i))
        callCode = str(instXAQueryT2301.GetFieldData("t2301OutBlock1", "optcode", i))
        putP = float(instXAQueryT2301.GetFieldData("t2301OutBlock2", "price", i))
        putCode = str(instXAQueryT2301.GetFieldData("t2301OutBlock2", "optcode", i))
        dif = abs(callP - putP);
        new_row = {'strike': actprice, 'call': callP, 'cCode': callCode, 'put': putP, 'pCode': putCode, 'LenCP': dif}
        op = op.append(new_row, ignore_index=True)

    op.set_index('strike', inplace=True)  # strike as an index
    return op


# ----------------------------------------------------------------------------
# T0441 계좌잔고
# ----------------------------------------------------------------------------
class XAQueryEventHandlerT0441:
    query_state = 0

    def OnReceiveData(self, code):
        XAQueryEventHandlerT0441.query_state = 1


def T0441(acn, pwd):
    XAQueryEventHandlerT0441.query_state = 0

    instXAQueryT0441 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEventHandlerT0441)
    instXAQueryT0441.ResFileName = "C:\\eBEST\\xingAPI\\Res\\T0441.res"
    instXAQueryT0441.SetFieldData("t0441InBlock", "accno", 0, acn)
    instXAQueryT0441.SetFieldData("t0441InBlock", "passwd", 0, pwd)
    instXAQueryT0441.Request(0)

    balance = DataFrame()

    while XAQueryEventHandlerT0441.query_state == 0:
        pythoncom.PumpWaitingMessages()

    count = instXAQueryT0441.GetBlockCount("t0441OutBlock1")

    for i in range(count):
        code = str(instXAQueryT0441.GetFieldData("t0441OutBlock1", "expcode", i))
        medosu = str(instXAQueryT0441.GetFieldData("t0441OutBlock1", "medosu", i))
        q = instXAQueryT0441.GetFieldData("t0441OutBlock1", "cqty", i)
        new_row = {'code': code, 'medosu': medosu, 'qty': q}
        balance = balance.append(new_row, ignore_index=True)
    return balance


# ----------------------------------------------------------------------------
# T1511 업종지수
# ----------------------------------------------------------------------------
class XAQueryEventHandlerT1511:
    query_state = 0

    def OnReceiveData(self, code):
        XAQueryEventHandlerT1511.query_state = 1


def T1511(code):
    XAQueryEventHandlerT1511.query_state = 0

    instXAQueryT1511 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEventHandlerT1511)
    instXAQueryT1511.ResFileName = "C:\\eBEST\\xingAPI\\Res\\t1511.res"
    instXAQueryT1511.SetFieldData("t1511InBlock", "upcode", 0, code)
    instXAQueryT1511.Request(0)

    while XAQueryEventHandlerT1511.query_state == 0:
        pythoncom.PumpWaitingMessages()

    price = float(instXAQueryT1511.GetFieldData("t1511OutBlock", "pricejisu", 0))
    return price