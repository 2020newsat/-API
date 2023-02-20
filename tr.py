from pandas import DataFrame
from query import *
from time import *



#BidAskTable
def BAT(code):
    query = XAQuery()
    query.register_res("t2105.res")
    query.set_field_data("t2105InBlock", "shcode", code)
    query.request()

    BidAsk = DataFrame()
    bid1 = float(query.get_field_data("t2105OutBlock", "bidho1"))
    bid2 = float(query.get_field_data("t2105OutBlock", "bidho2"))
    bid3 = float(query.get_field_data("t2105OutBlock", "bidho3"))
    ask1 = float(query.get_field_data("t2105OutBlock", "offerho1"))
    ask2 = float(query.get_field_data("t2105OutBlock", "offerho2"))
    ask3 = float(query.get_field_data("t2105OutBlock", "offerho3"))
    BidAsk = {'bid1': bid1, 'bid2': bid2, 'bid3': bid3, 'ask1': ask1, 'ask2': ask2, 'ask3': ask3}
    print(BidAsk)
    return BidAsk

def Bid1(code):
    query = XAQuery()
    query.register_res("t2105.res")
    query.set_field_data("t2105InBlock", "shcode", code)
    query.request()
    bid1 = query.get_field_data("t2105OutBlock", "bidho1")
    print("bid1: ",bid1)
    return bid1


# ----------------------------------------------------------------------------
# balance 계좌잔고확인
# ----------------------------------------------------------------------------
def ClearBalance(acn, pwd):
    query = XAQuery()
    query.register_res("t0441.res")
    dfs = query.block_request("t0441", accno=acn, passwd=pwd)
    balance = dfs[1]
    return balance


# 지수 확인 205
def index(upcode):
    query = XAQuery()
    query.register_res("t1511.res")
    query.set_field_data("t1511InBlock", "upcode", upcode)
    query.request()
    return float(query.get_field_data("t1511OutBlock", "pricejisu"))


# 옵션전광판
def op(Opym, OpGubun):
    query = XAQuery()
    query.register_res("t2301.res")
    opdf = query.block_request("t2301", yyyymm=Opym, gubun=OpGubun)
    # yyyymm: 미니, 일반은 yyyymm, 위클리는 'W1    '
    # gubun: 'W' weekly 'M' 미니 'G' 일반
    call = opdf[1]
    put = opdf[2]
    opt = DataFrame()

    for i in range(len(call)):
        strike = float(call.iloc[i, 0])
        callCode = call.iloc[i, 1]
        callP = float(call.iloc[i, 2])
        putCode = put.iloc[i, 1]
        putP = float(put.iloc[i, 2])
        dif = abs(callP - putP)
        new_row = {'strike': strike, 'cCode': callCode, 'call': callP, 'pCode': putCode, 'put': putP, 'LenCP': dif}
        opt = opt.append(new_row, ignore_index=True)

    opt['LenUD'] = 100
    row = len(opt.index) - 1
    for i in range(0, row):
        opt.iloc[i, 6] = abs(opt.iloc[i, 2] - opt.iloc[i + 1, 4])

    return opt

# ----------------------------------------------------------------------------
# RunOrder: tmCode - bid ask - enter
# ----------------------------------------------------------------------------
def runOrder(order, acn, passwd):

    print("order ready: ", order)
    print("range(len(order)), :",range(len(order)))

    for row in range(len(order)):
        code = order.iloc[row, 0]
        qty = int(order.iloc[row, 1])
        print("qty ", qty)
        BidAsk = BAT(code)  # bid/ask 매수/매도 3호가까지 확인

        if qty > 0:
            bns = '2'
            price = BidAsk['ask3']
        if qty < 0:
            bns = '1'
            qty = - qty
            price = BidAsk['bid3']

        if qty != 0:
            for OrdCount in range(qty):
                print("OrdCount, code, 1sell/2buy, price, row", OrdCount, code, bns, price, row)
                query = XAQuery()
                query.register_res("CFOAT00100.res")
                query.set_field_data("CFOAT00100InBlock1", "AcntNo", acn)
                query.set_field_data("CFOAT00100InBlock1", "Pwd", passwd)
                query.set_field_data("CFOAT00100InBlock1", "FnoIsuNo", code)
                query.set_field_data("CFOAT00100InBlock1", "BnsTpCode", bns)
                query.set_field_data("CFOAT00100InBlock1", "FnoOrdprcPtnCode", '00')
                query.set_field_data("CFOAT00100InBlock1", "FnoOrdPrc", price)
                query.set_field_data("CFOAT00100InBlock1", "OrdQty", 1)
                query.request()
                OrdNo = query.get_field_data("CFOAT00100OutBlock2", "OrdNo")
                sleep(1)
                print(OrdNo)

    # CFOAT00100(code, BnS, kind, price, qty) - return: OrdNo
    # BnS '1' 매도 '2' 매수
    # FnoOrdprcPtnCode '00' 지정가 / '03' 시장가



