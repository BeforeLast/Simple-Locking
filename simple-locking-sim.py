from os import name
from classes.Schedule import Schedule
from classes.Manager import Manager

if __name__ == '__main__':
    FILE_DIRECTORY = './test/Schedule1.csv'
    WRITE_LOG = True

    s = Schedule(FILE_DIRECTORY)
    m = Manager(s)

    m.manage_schedule(log=WRITE_LOG)