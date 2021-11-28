from typing import Dict
from classes.Constants import Constants
from classes.Operation import Operation
from classes.Schedule import Schedule
from classes.Lock import Lock
from typing import *

class Manager:
    schedule:List[Operation] = []
    executed_operation:List[Operation] = []
    lock:Dict[str,Lock] = {}
    queue:List[Operation] = []
    wait_graph:List[List[str]] = []

    def __init__(self,schedule:Schedule) -> None:
        self.schedule = schedule.get_schedule()
        for accessed_data in schedule.get_accessed_data():
            self.lock[accessed_data] = Lock(accessed_data,Constants.EXCLUSIVE)
    
    def manage_schedule(self):
        copy_schedule:Schedule = self.schedule.copy()
        self.print_splitter()
        while copy_schedule or self.queue:
            if self.queue and self.is_runnable(self.queue[0],True):
                # EXECUTE QUEUE
                operation = self.queue[0]
                self.queue = self.queue[1:]
                # COMMIT AND UNLOCK
                if operation.get_op() == Constants.COMMIT:
                    # Do Commit -> Unlock
                    for accessed_data in self.lock:
                        if self.lock[accessed_data].get_current_access() == operation.get_transaction():
                            self.lock[accessed_data].drop_current_access()
                # LOCK
                elif not self.lock[operation.get_target()].get_current_access():
                    # Lock is empty -> Lock
                    self.lock[operation.get_target()].set_current_access(operation.get_transaction())
                operation.print()
                print('REMAINING ',end='')
                self.print_queue()
                self.executed_operation.append(operation)
            else:
                # UNABLE TO EXECUTE QUEUE
                operation = copy_schedule[0]
                copy_schedule = copy_schedule[1:]
                if self.is_runnable(operation):
                    # COMMIT AND UNLOCK
                    if operation.get_op() == Constants.COMMIT:
                            # Do Commit -> Unlock
                            operation.print()
                            for accessed_data in self.lock:
                                if self.lock[accessed_data].get_current_access() == operation.get_transaction():
                                    self.lock[accessed_data].drop_current_access()
                    # LOCK AND EXECUTE
                    elif not self.lock[operation.get_target()].get_current_access():
                        # Lock still empty -> Lock -> Execute Operation
                        self.lock[operation.get_target()].set_current_access(operation.get_transaction())
                        operation.print()
                    elif self.lock[operation.get_target()].get_current_access() == operation.get_transaction():
                        # Lock is being hold by current operation transaction -> Execute Operation
                        operation.print()
                    self.executed_operation.append(operation)
                else:
                    # QUEUE
                    self.queue.append(operation)
                    self.print_queue()
                    
                    # # CHECK IF DEADLOCK
                    # if operation.get_target():
                    #     pass
                    # pass
            self.print_splitter()
            
    # def check_deadlock(self):
    #     pass

    
    def is_runnable(self,operation:Operation,dequeue:bool=False):
        """Check if operation can be executed from lock"""
        runnable_dequeue = True
        # Check Queue (if not dequeue process)
        if not dequeue:
            for op in self.queue:
                if op.get_transaction() == operation.get_transaction():
                    runnable_dequeue = False
                    break
        
        # Check Lock
        if operation.get_op() == Constants.COMMIT:
            return runnable_dequeue
        return (self.lock[operation.get_target()].get_current_access() == None or self.lock[operation.get_target()].get_current_access() == operation.get_transaction()) and runnable_dequeue

    def print_queue(self):
        if self.queue:
            print("QUEUE: " + ', '.join([i.toString() for i in self.queue]))
        else:
            print("QUEUE: Nothing")
        

    def check_queue(self):
        for key in self.queue:
            if self.queue[key] == None or len(self.queue[key]) == 0:
                return True
        return False
    
    def print_splitter(self):
        print("="*32)
