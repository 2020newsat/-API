import win32com.client
import pythoncom
import datetime
from pandas import Series, DataFrame


class XASessionEventHandler:
    login_state = 0

    def OnLogin(self, code, msg):
        if code == "0000":
            print("로그인 성공")
            XASessionEventHandler.login_state = 1
        else:
            print("로그인 실패")


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


# ----------------------------------------------------------------------------
# T2301 옵션전광판
# ----------------------------------------------------------------------------

class XAQueryEventHandlerT2301:
    query_state = 0

    def OnReceiveData(self, code):
        XAQueryEventHandlerT2301.query_state = 1


def T2301(ymd):
    XAQueryEventHandlerT2301.query_state = 0
    instXAQueryT2301 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEventHandlerT2301)
    instXAQueryT2301.ResFileName = "C:\\eBEST\\xingAPI\\Res\\t2301.res"

    instXAQueryT2301.SetFieldData("t2301InBlock", "yyyymm", 0, ymd)
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
# T2105 옵션호가
# ----------------------------------------------------------------------------
class XAQueryEventHandlerT2105:
    query_state = 0

    def OnReceiveData(self, code):
        XAQueryEventHandlerT2105.query_state = 1


def T2105(code):
    XAQueryEventHandlerT2105.query_state = 0

    instXAQueryT2105 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEventHandlerT2105)
    instXAQueryT2105.ResFileName = "C:\\eBEST\\xingAPI\\Res\\t2105.res"
    instXAQueryT2105.SetFieldData("t2105InBlock", "shcode", 0, code)
    instXAQueryT2105.Request(0)

    while XAQueryEventHandlerT2105.query_state == 0:
        pythoncom.PumpWaitingMessages()

    BidAsk = DataFrame()
    bid1 = float(instXAQueryT2105.GetFieldData("t2105OutBlock", "bidho1", 0))
    bid2 = float(instXAQueryT2105.GetFieldData("t2105OutBlock", "bidho2", 0))
    bid3 = float(instXAQueryT2105.GetFieldData("t2105OutBlock", "bidho3", 0))
    ask1 = float(instXAQueryT2105.GetFieldData("t2105OutBlock", "offerho1", 0))
    ask2 = float(instXAQueryT2105.GetFieldData("t2105OutBlock", "offerho2", 0))
    ask3 = float(instXAQueryT2105.GetFieldData("t2105OutBlock", "offerho3", 0))
    BidAsk = {'bid1': bid1, 'bid2': bid2, 'bid3': bid3, 'ask1': ask1, 'ask2': ask2, 'ask3': ask3}
    return BidAsk


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
        q = int(instXAQueryT0441.GetFieldData("t0441OutBlock1", "cqty", i))
        new_row = {'code': code, 'medosu': medosu, 'qty': q}
        balance = balance.append(new_row, ignore_index=True)
    return balance


# ----------------------------------------------------------------------------
# CFOAT00100: order
# ----------------------------------------------------------------------------
class XAQueryEventHandlerCFOAT00100:
    query_state = 0

    def OnReceiveData(self, code):
        XAQueryEventHandlerCFOAT00100.query_state = 1


def CFOAT00100(code, BnS, kind, price, qty):
    instXAQueryCFOAT00100 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEventHandlerCFOAT00100)
    instXAQueryCFOAT00100.ResFileName = "C:\\eBEST\\xingAPI\\Res\\CFOAT00100.res"
    XAQueryEventHandlerCFOAT00100.query_state = 0

    instXAQueryCFOAT00100.SetFieldData("CFOAT00100InBlock1", "AcntNo", 0, acn)
    instXAQueryCFOAT00100.SetFieldData("CFOAT00100InBlock1", "Pwd", 0, passwd)
    instXAQueryCFOAT00100.SetFieldData("CFOAT00100InBlock1", "FnoIsuNo", 0, code)
    instXAQueryCFOAT00100.SetFieldData("CFOAT00100InBlock1", "BnsTpCode", 0, BnS)
    instXAQueryCFOAT00100.SetFieldData("CFOAT00100InBlock1", "FnoOrdprcPtnCode", 0, kind)
    instXAQueryCFOAT00100.SetFieldData("CFOAT00100InBlock1", "FnoOrdPrc", 0, price)
    instXAQueryCFOAT00100.SetFieldData("CFOAT00100InBlock1", "OrdQty", 0, qty)
    instXAQueryCFOAT00100.Request(0)

    while XAQueryEventHandlerCFOAT00100.query_state == 0:
        pythoncom.PumpWaitingMessages()

    OrdNo = instXAQueryCFOAT00100.GetFieldData("CFOAT00100OutBlock2", "OrdNo", 0)
    return (OrdNo)


# ----------------------------------------------------------------------------
# tmCode: 옵션 행사가, 코드 반환 함수
# ----------------------------------------------------------------------------
def tmCode(atm, tm, cp):
    if cp == 'p':
        tm = -tm
    strike = atm + tm * 2.5
    cCode = op.loc[strike, 'cCode'].iloc[0]
    pCode = op.loc[strike, 'pCode'].iloc[0]
    if cp == 'c':
        code = cCode
    if cp == 'p':
        code = pCode
    return strike, code


# ----------------------------------------------------------------------------
# OneStopOrder: tmCode - bid ask - enter
# ----------------------------------------------------------------------------
def OneStopOrder(atm, tm, cp, bs):
    (strike, code) = tmCode(atm, tm, cp)
    BidAsk = T2105(code)  # bid/ask 매수/매도 3호가까지 확인

    if bs == 's':
        bns = '1'
        price = BidAsk['bid3']
    if bs == 'b':
        bns = '2'
        price = BidAsk['ask3']

    print(price)
    OrdNo = CFOAT00100(code, bns, '00', price, 1)
    print(OrdNo)


# CFOAT00100(code, BnS, kind, price, qty) - return: OrdNo
# BnS = '2'  # BnsTpCode 1 매도 2 매수
# kind '00' 지정가 / '03' 시장가
# OrdNo = CFOAT00100(code, '1', '03',0, 1)


# ----------------------------------------------------------------------------
# CodeToStrike 종목코드로 행사가, 콜풋 여부 찾기
# ----------------------------------------------------------------------------

# 0  201T2330  매수  1.0
# 1  201T2332  매도  1.0
# 2  301T2317  매도  1.0
# 3  301T2320  매수  1.0

def CodeToStrike(code):
    print(code)
    if code[0] == '2':
        cp = 'c'
    if code[0] == '3':
        cp = 'p'

    strike = float(code[5:])
    if strike % 5 > 0:
        strike = strike + 0.5

    print(strike)
    return strike, cp


# ----------------------------------------------------------------------------
# login
# ----------------------------------------------------------------------------
id = ' '
passwd = ' '
cert_passwd = "공인인증서"

instXASession = win32com.client.DispatchWithEvents("XA_Session.XASession", XASessionEventHandler)
instXASession.ConnectServer("demo.ebestsec.co.kr", 20001)
instXASession.Login(id, passwd, cert_passwd, 0, 0)

# 접속할 서버의 기본 주소는 'hts.ebestsec.co.kr'
# 모의 투자인 경우에는 'demo.ebestsec.co.kr'

while XASessionEventHandler.login_state == 0:
    pythoncom.PumpWaitingMessages()

acn = '55501135251'  # account number
pwd = '0000'  # password

today = datetime.datetime.today()
ymd = today.strftime("%Y%m")
print(ymd)

# 101 kp200
# 205 vkospi
kp200 = T1511(101)
vkospi = T1511(205)


op = T2301(ymd)

nearKp200 = int(kp200 * 0.4) / 0.4

balance = T0441(acn, pwd)

for i in range(len(balance)):
    code = balance.iloc[i, 0]
    (strike, cp) = CodeToStrike(code)

    if balance.iloc[i, 1] == '매수':
        bs = 's'
    if balance.iloc[i, 1] == '매도':
        bs = 'b'

    if cp == 'c':
        tm = (strike - atm) / 2.5

    if cp == 'p':
        tm = (strike - atm) / -2.5

    #    print("tm, cp, bs: ", tm, cp, bs)
    OrderNo = OneStopOrder(atm, tm, cp, bs)

w = today.weekday()
# 0 ~ 4 월 ~ 금
