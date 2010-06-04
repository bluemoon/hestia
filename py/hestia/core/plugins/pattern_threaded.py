import sys
import inspect
import time

class threading_pattern:
    def __init__(self, child=None, parent=None):
        self.child_connection = child
        self.parent_queue     = parent

    def main(self):
        pass
    
    def run(self, lock, child_connection, parent_queue):
        self.child_connection = child_connection
        self.lock = lock
        self.parent_queue = parent_queue
        #self.main()
        keep_running = True
        while keep_running:
            time.sleep(0.12)
            if self.child_connection.poll():
                msg = self.child_connection.recv()
                if msg == 'quit':
                    keep_running = False
                    sys.exit()
                elif msg == 'dict':
                    self.lock.acquire()
                    self.parent_queue.put(self.__dict__)
                    self.child_connection.send(self.__dict__)
                    self.lock.release()
                else:
                    runner = getattr(self, msg)
                    if inspect.isfunction(runner):
                        child_connection.send(repr(runner()))
                    else:
                        child_connection.send(runner)
                    #data = 'process %s: %s\n' % (multiprocessing.current_process(), runner)
                    #lock.release()

                    
             
