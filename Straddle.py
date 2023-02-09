def Straddle(tm1, op, order):
    # short call
    strike = atm + tm1 * 2.5
    code = StrikeToCode(strike, op, 'c')
    order = SetOrder(code, 1, 's', order)

    # short put
    strike = atm - tm1 * 5
    code = StrikeToCode(strike, op, 'p')
    order = SetOrder(code, 1, 's', order)

    return