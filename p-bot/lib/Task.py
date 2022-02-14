class Task():
    tasks = []

    def __init__(self, id, progress_callback):
        self.active = False
        self.id = id
        self.progress_callback = progress_callback
        self.progress = 0
        Task.tasks.append(self)

    def startTask(self, **kwargs):
        self.active = True

        no_of_packets = kwargs.get('no_of_packets', None)
        target_ip = kwargs.get('target_ip', None)
        dport = kwargs.get('dport', None)
        sport = kwargs.get('sport', None)
        self.doTask(no_of_packets=no_of_packets,
                    target_ip=target_ip, dport=dport, sport=sport)

    def stopTask(self):
        self.active = False

    def progressUpdateCallBack(self):
        self.progress_callback(self.progress)

    def doTask(self):
        raise NotImplementedError("Please Implement this method")
