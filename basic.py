from pandas import DataFrame
import datetime

from session import *
from query import *
from etc import *
from wait import *
from tr import *

# parameter id, passwd, cert, acn etc
id
passwd
cert =
acn = # 계좌번호
pwd = '0000'  # 계좌비번
qty = 2
Opym = 'W4    '
OpGubun = 'W'
today = datetime.datetime.today()
ymd = today.strftime("%Y%m")
w = today.weekday()

# 로그인 (Session)
print("login requst")
session = XASession()
session.login(id, passwd, cert, block=True)
print("login done")
acc = session.get_account_list(0)
print(acc)

# ----------------------------------------------------------------------------
# T0441 계좌잔고확인
# ----------------------------------------------------------------------------
balance = DataFrame()
balance = ClearBalance(acn, pwd)
print(balance)

# ----------------------------------------------------------------------------
# 잔고청산
# ----------------------------------------------------------------------------
order = DataFrame()
for i in range(len(balance)):
    code = balance.iloc[i, 0]
    q = int(balance.iloc[i, 2])
    if balance.iloc[i, 1] == '매수':
        bns = 's'
    if balance.iloc[i, 1] == '매도':
        bns = 'b'

    order = SetOrder(code, q, bns, order)

# 요일확인, 동시호가 대기
w = today.weekday()
WaitUntil()
# Option Price Table
# strike     cCode   call     pCode    put  LenCP   LenUD

opt = DataFrame()
opt = op(Opym, OpGubun)
print(opt)

# calculate ATM
minUD = opt['LenUD'].min()
print(minUD)
Uindex = opt.loc[opt['LenUD'] == minUD].index[0]
Ulen = opt.iloc[Uindex, 5]
Dlen = opt.iloc[Uindex + 1, 5]
Mlen = min(Ulen, Dlen)

if minUD <= Mlen:
    c1 = opt.iloc[Uindex, 0]
    p1 = c1 - 2.5
else:
    c1 = opt.loc[opt['LenCP'] == Mlen].strike.iloc[0]+2.5
    p1 = c1 - 5
print(c1, p1)

# Strategy

# 세팅된 주문 실행
runOrder(order, acn, passwd)
