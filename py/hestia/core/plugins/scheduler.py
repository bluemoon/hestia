import sched
import time

from multiprocessing import Queue, Process
from multiprocessing.queue import Empty


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

QUEUE = Queue() # Message queue.  Use `enqueue` to add messages.
TIMEOUT = 10 # Seconds for scheduler to wait for items in queue.
SCHEDULER = Scheduler(QUEUE, handle) # Message handler scheduler.
PROCESS = None # Process running the scheduler.

def enqueue(message):
    global PROCESS
    QUEUE.put(message)
    if PROCESS is None or PROCESS.getExitCode() is not None:
        # There is no scheduler process running; start one.
        PROCESS = Process(target=run_scheduler, args=(SCHEDULER,))
        PROCESS.start()
