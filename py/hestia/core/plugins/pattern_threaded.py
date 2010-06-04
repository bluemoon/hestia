import sys
import inspect

class threading_pattern:
    def setUp(self, child_connection, parent_queue):
        self.__child_connection = child_connection
        self.__parent_queue = parent_queue
        
    def run(self, lock, child_connection, parent_queue):
        keep_running = True
        while keep_running:
            if child_connection.poll():
                msg = child_connection.recv()
                if msg == 'quit':
                    keep_running = False
                    sys.exit()
                elif msg == 'dict':
                    lock.acquire()
                    parent_queue.put(self.__dict__)
                    child_connection.send(self.__dict__)
                    lock.release()
                else:
                    runner = getattr(self, msg)
                    if inspect.isfunction(runner):
                        child_connection.send(repr(runner()))
                    else:
                        child_connection.send(runner)
                    #data = 'process %s: %s\n' % (multiprocessing.current_process(), runner)
                    #lock.release()

                    
             
