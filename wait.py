import win32com.client
import pythoncom
import pandas

from threading import Thread
from queue import Queue
from pyxing import res


class XARealEvents:
    def __init__(self):
        self.com_obj = None
        self.user_obj = None
        self.queue = None

    def OnReceiveRealData(self, trcode):
        res_data = self.user_obj.res.get(trcode)
        out_data = {}

        out_block = res_data['outblock'][0]

        for field in out_block['OutBlock']:
            data = self.user_obj.get_field_data(field)
            out_data[field] = data

        out_data_list = [out_data]
        df = pandas.DataFrame(data=out_data_list)
        self.queue.put((trcode, df))

    def connect(self, com_obj, user_obj, queue):
        self.com_obj = com_obj
        self.user_obj = user_obj
        self.queue = queue


class XAReal:
    def __init__(self, queue):
        self.com_obj = win32com.client.Dispatch("XA_DataSet.XAReal")  # COM 객체 생성
        self.event_handler = win32com.client.WithEvents(self.com_obj, XARealEvents)  # 이벤트 처리 클래스 연결
        self.event_handler.connect(self.com_obj, self, queue)
        self.res = {}

    def register_res(self, res_file):
        """
        RES 파일 등록
        :param res_file: res 파일 (JIF.res)
        :return:
        """
        # Res 파일 등록
        res_name = res_file[:-4]
        res_path = "C:\\eBEST\\xingAPI\\Res\\" + res_file
        self.com_obj.ResFileName = res_path

        # Res 파일 파싱
        with open(res_path, encoding="euc-kr") as f:
            res_lines = f.readlines()
            res_data = res.parse_res(res_lines)
            self.res[res_name] = res_data

    def set_field_data(self, field, data):
        ret = self.com_obj.SetFieldData("InBlock", field, data)

    def advise_real_data(self):
        ret = self.com_obj.AdviseRealData()

    def get_field_data(self, field):
        data = self.com_obj.GetFieldData("OutBlock", field)
        return data

    def unadvise_real_data(self):
        """
        실시간 데이터 요청 취소
        :return:
        """
        self.com_obj.UnadviseRealData()


# 데이터를 소비하는 스레드
def consumer(in_q, x):
    while 1:
        data = in_q.get()
        time = int(data[1]['time'].iloc[0])%100
        x.append(time)


def WaitUntil():
    # 스레드간 데이터 전달을 위한 Queue 객체 생성하기
    queue = Queue()
    x = []

    xareal = XAReal(queue)
    xareal.register_res("IJ_.res")
    xareal.set_field_data("upcode", "101")
    xareal.advise_real_data()

    # 데이터를 소비하는 스레드 시작
    t2 = Thread(target=consumer, args=(queue, x))
    t2.daemon = True
    t2.start()

    while 1:
        if len(x) > 0:
            t = x.pop()
            print(t)
            if t > 70:
                return
        pythoncom.PumpWaitingMessages()