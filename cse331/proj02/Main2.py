#!/usr/bin/python3

from Deque import Deque


def main(filename):
    deque = Deque()
    print(deque.length)
    with open(filename, 'r') as reader:
        for line in reader:
            line = line.strip()
            if line.startswith('+f'):
                deque.push_front(line.split()[1])
            elif line.startswith('+b'):
                deque.push_back(line.split()[1])
            elif line == '-f':
                deque.pop_front()
            elif line == '-b':
                deque.pop_back()
            elif line == 'clear':
                deque.clear()
            elif line == 'print':
                print(deque)
            elif line == 'len':
                print('length:', len(deque))
            elif line.startswith('count'):
                deque.count_if(lambda s : line.split()[1] in s)
            elif line.startswith('keep'):
                deque.keep_between(int(line.split()[1]),int(line.split()[2]))
            else:
                raise KeyError(line)


if __name__ == '__main__':
    main('example.txt')
