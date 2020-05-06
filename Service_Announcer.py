import os
import glob
import json
import socket
import threading
import time
from datetime import timedelta


port = 5000
username = ""
MAX_BYTES = 65535


class Job(threading.Thread):
    def __init__(self, interval, execute, *args, **kwargs):
        threading.Thread.__init__(self)
        self.daemon = False
        self.stopped = threading.Event()
        self.interval = interval
        self.execute = execute
        self.args = args
        self.kwargs = kwargs

    def stop(self):
        self.stopped.set()
        self.join()

    def run(self):
        while not self.stopped.wait(self.interval.total_seconds()):
            self.execute(*self.args, **self.kwargs)


class AnnouncerJob(Job):
    def __init__(self, announcer, service_dict):
        Job.__init__(self, timedelta(seconds=10), execute=announce,
                     socket=announcer, service_dict=service_dict)
        self.service_dict = service_dict
        self.announcer = announcer
        return

    def update(self, service_dict):
        self.stop()
        self.__init__(self.announcer, service_dict)
        return


def announce(socket, service_dict):
    service = json.dumps(service_dict)
    socket.sendto(bytes(service, "utf-8"), ("<broadcast>", port))
    print("Last sent was at ",
          time.ctime())
    print(service_dict["files"])
    return


def read_files():
    # TODO: Make it read only the names of the files 
    # since it will contain the chunks
    filenames = os.listdir("files")  # read all files in the directory
    filenames_json = json.dumps(filenames)  # convert JSON array.
    return filenames_json


def main():
    # get files
    username = input("Your username:")
    announcer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    announcer.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    file_list = read_files()
    service_dict = {"username": username, "files": file_list}
    job = AnnouncerJob(announcer, service_dict)
    job.start()
    # main loop
    while True:
        try:
            new_file_list = read_files()
            if new_file_list != file_list:
                service_dict["files"] = new_file_list
                job.update(service_dict)
                job.start()

            # Announce and wait 10 seconds
            #  announce(announcer, service_dict)
            #  time.sleep(10)
            #  job = Job(interval=timedelta(seconds=WAIT_TIME_SECONDS),
            #            execute=announce, socket=announcer, service_dict=service_dict)
            #  job.start()

        except Exception as e:
            print(str(e))
            pass


if __name__ == "__main__":
    main()
