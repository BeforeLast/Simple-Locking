from classes.Constants import Constants


class Lock:
    data = None
    type = None
    current_access = None

    def __init__(self,data:str,type:str) -> None:
        self.data = data
        self.type = type
    
    def set_current_access(self,transaction:str):
        """Set current data access to transaction"""
        self.current_access = transaction
        if self.type == Constants.EXCLUSIVE:
            print(f'GRANT EXCLUSIVE LOCK ON {self.data} TO {self.current_access}')
        elif self.type == Constants.SHARED:
            print(f'GRANT SHARED LOCK ON {self.data} TO {self.current_access}')
    
    def drop_current_access(self):
        """Disable data access to any transaction"""
        self.current_access = None
        print(f'UNLOCK {self.data}')

    def get_current_access(self):
        """Get transaction that hold current access to data"""
        return self.current_access
    
    def toString(self):
        if self.current_access:
            return f'Transaction {self.current_access} currently holding the {self.type} lock for {self.data}'
        else:
            return f'No transaction currently holding the {self.type} lock for {self.data}'

    # def print(self):
    #     if not self.current_access:
    #         print(f'UNLOCK {self.data}')
    #     if self.type == Constants.EXCLUSIVE:
    #         print(f'GRANT EXCLUSIVE LOCK ON {self.data} TO {self.current_access}')
    #     elif self.type == Constants.SHARED:
    #         print(f'GRANT SHARED LOCK ON {self.data} TO {self.current_access}')
