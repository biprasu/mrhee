#encoding=utf8
import re

#utility functions for rhee

def MapBreakPoints(breakpoints, filename):
    #Read the filename, extract line number and return line number map
    f = open(filename, 'r')
    file_line = 0
    pytorhee = []
    rheetopy = []
    while True:
        l = f.readline()
        if not l: break

        rhee_line = re.findall('#(\d+)$', l)
        if rhee_line:
            pytorhee.append((file_line, int(rhee_line[0])-1))
            rheetopy.append((int(rhee_line[0])-1, file_line))
        file_line += 1
    return dict(pytorhee), dict(rheetopy)


if __name__ == '__main__':
    print MapBreakPoints([], 'Rhee_Files/temp.py')

