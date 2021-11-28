import csv
from classes.Operation import Operation
from classes.Constants import Constants


class Schedule:
    trasanction_name = []
    data = []
    schedule = []
    accessed_data = []

    def __init__(self,filepath:str=None) -> None:
        if filepath != None:
            with open(filepath,mode='r',newline='') as f:
                data = list(csv.reader(f,delimiter=','))
                self.trasanction_name = data[0]
                self.data = data[1:]
                if (len(set(self.trasanction_name)) < len(self.trasanction_name)):
                    raise ValueError('Duplicate Transaction Name Found')
                for row in self.data:
                    for i in range(len(self.trasanction_name)):
                        if not row[i]:
                            continue
                        if row[i].find('(') == -1:
                            opname = row[i]
                        else:
                            opname = row[i][:row[i].find('(')]
                        temp_operation = None
                        if opname == Constants.WRITE:
                            data_access = row[i][row[i].find('(')+1:row[i].find(')')]
                            temp_operation = Operation(Constants.WRITE,self.trasanction_name[i],data_access)
                            self.accessed_data.append(data_access)
                        elif opname == Constants.READ:
                            data_access = row[i][row[i].find('(')+1:row[i].find(')')]
                            temp_operation = Operation(Constants.READ,self.trasanction_name[i],data_access)
                            self.accessed_data.append(data_access)
                        elif opname == Constants.COMMIT:
                            temp_operation = Operation(Constants.COMMIT,self.trasanction_name[i])
                        self.schedule.append(temp_operation)
                self.accessed_data = list(set(self.accessed_data))

    def get_schedule(self):
        return self.schedule

    def get_accessed_data(self):
        return self.accessed_data

    def toString(self):
        for i in self.schedule:
            print(i.toString())
        schedule_str = [data.toString() for data in self.schedule]
        return ', '.join(schedule_str)

    def copy(self):
        result = Schedule()
        result.trasanction_name = self.trasanction_name[:]
        result.accessed_data = self.accessed_data[:]
        result.data = self.data[:]
        result.schedule = self.schedule[:]
        return result



if __name__=='__main__':
    s = Schedule('./test/Schedule1.csv')