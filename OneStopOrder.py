
# ----------------------------------------------------------------------------
# OneStopOrder: tmCode - bid ask - enter
# ----------------------------------------------------------------------------
def OneStopOrder(tm, cp, bs):
    (strike, code) = tmCode(tm, cp)
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
    return

# CFOAT00100(code, BnS, kind, price, qty) - return: OrdNo
# BnS = '2'  # BnsTpCode 1 매도 2 매수
# kind '00' 지정가 / '03' 시장가
# OrdNo = CFOAT00100(code, '1', '03',0, 1)
