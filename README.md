# Simple-Locking

## Requirement
- Python 3.9.7+

## How to Run
### Running the Program
1. Change variable FILE_DIRECTORY inside simple-locking-sim.py
2. Run simple-locking-sim.py using Python

note: to create log, change variable WRITE_LOG to True
### Creating Task
1. Create a csv file (use google sheets -> save as csv)
2. The first row should indicate the transaction id/name
3. The remaining row(s) should only have one operation for all column(s)
4. Every transaction need to have at least a commit at the end of the transaction

note: for example, see file Schedule1.csv inside folder test