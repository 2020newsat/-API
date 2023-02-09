# ----------------------------------------------------------------------------
# T2105 옵션호가
# ----------------------------------------------------------------------------
import win32com.client
import pythoncom
from pandas import Series, DataFrame

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
