#!/usr/bin/python3

from Heap import find_median


def main(filename):
    with open(filename, 'r') as reader:
        text = [line.strip() for line in reader]
        median = find_median(text)
        print('Median:', median)


if __name__ == '__main__':
    main('alphabet.txt')
