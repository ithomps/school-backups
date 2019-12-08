"""
Lis.py
Author: Ian Thompson
04/26/2019
"""


def verify_subseq(seq, subseq):
    """
    Determines if a sequence is a valid sub-sequence
    of another given sequence
    :param seq: Larger sequence
    :param subseq: Potential sub-sequence
    :return: If the sub-sequence is valid
    """
    found = False
    index = 0

    for item in subseq:
        while index < len(seq):  # search up until end of larger sequence
            if item == seq[index]:
                index += 1  # current item found, start looking for next
                found = True
                break
            else:
                index += 1
        if not found:
            return False  # item couldn't be found in larger sequence
        else:
            found = False  # reset to start looking for next item

    return True


def verify_increasing(seq):
    """
    Determines if a given sequence is in increasing order
    :param seq: Input sequence
    :return: Whether it is a valid increasing sequence
    """
    if not seq:  # Empty sequence
        return True

    prev = seq[0]
    for item in seq[1:]:  # Skip first index
        if item > prev:
            prev = item  # replace prev with item and start again
        else:
            return False

    return True


def find_lis(seq):
    """
    Determines the longest increasing sub-sequence
    Uses the solitaire like approach
    :param seq: Input sequence
    :return: Longest increasing sub-sequence of seq
    """
    final = []  # Holds reversed list of values
    ans = []  # Used to return final answer
    solitaire = []  # List of tuples
    prev = '-'
    inserted = False

    for item in seq:

        if not solitaire:  # solitaire structure is empty
            solitaire.append([(item, prev)])
        else:
            for pile in solitaire:  # checks piles from left to right

                if pile[-1][0] > item:  # checks the bottom item of each pile
                    if prev == item:  # duplicate is already at the top of a pile
                        inserted = True
                        break
                    pile.append((item, prev))  # insert at bottom of pile
                    inserted = True
                    break
                else:
                    prev = pile[-1][0]  # check next pile and change previous pointer

            if not inserted:  # won't fit on any current pile

                if item != prev:
                    solitaire.append([(item, prev)])  # make new pile
                prev = '-'
            else:
                prev = '-'  # case where item is a unnecessary duplicate
                inserted = False

    # Assemble longest increasing sub-sequence from the list of tuples
    next_t = '-'
    for tup in reversed(solitaire):  # reverse list

        if not final:
            final.append(tup[-1][0])  # enter the bottom card of the last pile
            next_t = tup[-1][1]  # uses pointer to the top of last pile at time of insertion
        else:
            for t in tup:  # iterate through cards in pile looking for the saved "prev" card
                if t[0] == next_t:
                    final.append(t[0])  # add to final
                    next_t = t[1]  # save new "prev" pointer
                    break

    # Put list into increasing order
    for val in reversed(final):
        ans.append(val)
    return ans
