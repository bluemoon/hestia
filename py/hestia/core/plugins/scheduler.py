from threading import Event, Thread
from multiprocessing import Queue, Process
from threading import Timer
from Queue import Empty
from collections import deque

import sched
import time


 
class RepeatTimer(Thread):
    def __init__(self, interval, function, iterations=0, args=[], kwargs={}):
        Thread.__init__(self)
        self.interval = interval
        self.function = function
        self.iterations = iterations
        self.args = args
        self.kwargs = kwargs
        self.finished = Event()
 
    def run(self):
        count = 0
        while not self.finished.is_set() and (self.iterations <= 0 or count < self.iterations):
            self.finished.wait(self.interval)
            if not self.finished.is_set():
                self.function(*self.args, **self.kwargs)
                count += 1
 
    def cancel(self):
        self.finished.set()

class scheduler:
    def __init__(self):
        self.tasks = {}
        self.timing_interval = 0.5
        self.work_queue    = deque([])
        self.process_queue = deque([])
        self.repeating = RepeatTimer(self.timing_interval, self.do_work)
        
    def do_work(self):
        work = self.work_queue.popleft()
        self.process_queue.push(Process(target=work).start())
        self.work_queue.push(work)
        
    def add_work(self, function):
        self.work_queue.push(function)


TIMEOUT = 10

def delay_put(duration, queue, message):
    time.sleep(duration)
    queue.put(message)
    queue.close()

class Scheduler(sched.scheduler):
    def __init__(self, queue, handler):
        delayfunc = self.make_delay_func(queue, handler)
        sched.scheduler.__init__(self, time.time, delayfunc)

    def make_delay_func(self, queue, handler):
        def delay(duration):
            if duration > 0:
                # Spawn a process that will sleep, enqueue None, and exit.
                Process(target=delay_put, args=(duration, queue, None)).start()
            try:
                message = queue.get(True, duration + TIMEOUT) # Block!
            except Empty:
                print "Timed out."
            else:
                if message is not None:
                    # A message was enqueued during the delay.
                    timestamp = message.get('timestamp', time.time())
                    priority = message.get('priority', 1)
                    self.enterabs(timestamp, priority, handler, (message,))
        return delay

    def startup(self):
        print "Starting scheduler!"

    def run(self):
        # Schedule the `startup` event to trigger `delayfunc`.
        self.enter(0, 0, self.startup, ())
        sched.scheduler.run(self)

def handle(message):
    print "[%s] MESSAGE: %s" % (time.time(), message)

def run_scheduler(scheduler):
    scheduler.run()
    print "Scheduler done."

#QUEUE = Queue() # Message queue.  Use `enqueue` to add messages.
#TIMEOUT = 10 # Seconds for scheduler to wait for items in queue.
#SCHEDULER = Scheduler(QUEUE, handle) # Message handler scheduler.
#PROCESS = None # Process running the scheduler.

def enqueue(message):
    global PROCESS
    QUEUE.put(message)
    if PROCESS is None or PROCESS.getExitCode() is not None:
        # There is no scheduler process running; start one.
        PROCESS = Process(target=run_scheduler, args=(SCHEDULER,))
        PROCESS.start()
