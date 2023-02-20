from tr import *


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
def StrikeToCode(strike, opt, cp):
    # print(opt, strike)
    cCode = opt.loc[opt['strike'] == strike, 'cCode'].iloc[0]
    pCode = opt.loc[opt['strike'] == strike, 'pCode'].iloc[0]
    print("cCode, pCode: ", cCode, pCode)
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
    # print("order set:", order)
    return order


def beep():
    fr = 2000  # range : 37 ~ 32767
    du = 1000  # 1000 ms ==1second
    sd.Beep(fr, du)  # winsound.Beep(frequency, duration)
    return


#
# 양매도 주문
#

def TMshort(qty, c1, p1, order, opt, n):
    if n == 0 and c1 < p1 + 3:
        return order

    n = n - 1
    cCode = StrikeToCode(c1 + 2.5 * n, opt, 'c')
    pCode = StrikeToCode(p1 - 2.5 * n, opt, 'p')
    callBid = float(Bid1(cCode))
    putBid = float(Bid1(pCode))

    if callBid < 0.1 or putBid < 0.1:
        return order
    else:
        order = SetOrder(cCode, qty, 's', order)
        order = SetOrder(pCode, qty, 's', order)
        return order




