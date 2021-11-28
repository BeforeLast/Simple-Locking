from classes.Constants import Constants

class Operation:
    operation_type = None
    transaction = None
    target = None
    def __init__(self,op:str,trn:str,trg:str=None) -> None:
        self.operation_type = op
        self.transaction = trn
        self.target = trg
    
    def get_op(self):
        return self.operation_type
    
    def get_transaction(self):
        return self.transaction
    
    def get_target(self):
        return self.target

    def toString(self):
        if self.target == None:
            return f'{self.operation_type}_{self.transaction}'
        else:
            return f'{self.operation_type}_{self.transaction}({self.target})'
    
    def print(self):
        if self.operation_type == Constants.WRITE:
            print(f'{self.transaction} WRITE {self.target}')
        elif self.operation_type == Constants.READ:
            print(f'{self.transaction} READ {self.target}')
        elif self.operation_type == Constants.COMMIT:
            print(f'COMMIT {self.transaction}')
        else:
            print('ERROR: UNKNOWN OPERATION')