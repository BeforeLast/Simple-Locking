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

    def __init__(self,schedule:Schedule) -> None:
        self.schedule = schedule.get_schedule()
        for accessed_data in schedule.get_accessed_data():
            self.lock[accessed_data] = Lock(accessed_data,Constants.EXCLUSIVE)
    
    def manage_schedule(self):
        copy_schedule:Schedule = self.schedule.copy()
        self.print_splitter()
        while copy_schedule or self.queue:
            if not copy_schedule and self.queue and not self.is_runnable(self.queue[0],True):
                # DEADLOCK DETECTED
                # Schedule empty and cannot execute first operation in queue
                # Rollback Process
                transaction_name = self.queue[0].get_transaction()
                print('DEADLOCK DETECTED')
                print(f'ROLLBACK ON TRANSACTION {transaction_name}')
                temp_rollback_schedule:List[Operation] = []
                temp_schedule:List[Operation] = []
                
                for op in self.executed_operation:
                    if op.get_transaction() == transaction_name:
                        temp_rollback_schedule.append(op)
                    else:
                        temp_schedule.append(op)
                self.executed_operation = temp_schedule[:]
                temp_schedule:List[Operation] = []
                for op in self.queue:
                    if op.get_transaction() == transaction_name:
                        temp_rollback_schedule.append(op)
                    else:
                        temp_schedule.append(op)
                for op in temp_rollback_schedule:
                    for accessed_data in self.lock:
                        if self.lock[accessed_data].get_current_access() == op.get_transaction():
                            self.lock[accessed_data].drop_current_access()
                self.queue = temp_schedule[:] + temp_rollback_schedule
            elif self.queue and self.is_runnable(self.queue[0],True):
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
        print("EXECUTED OPERATION: " + ', '.join([i.toString() for i in self.executed_operation]))

    
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
