from classes.Schedule import Schedule
from classes.Manager import Manager

s = Schedule('./test/Schedule2.csv')
m = Manager(s)

# print(m.lock)
m.manage_schedule()