# ----------------------------------------------------------------------------
# CFOAT00100: order
# ----------------------------------------------------------------------------
import win32com.client
import pythoncom

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
