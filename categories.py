from collections import Counter


def n_of_kind(nums, times):

    c = Counter(nums)
    for i, j in c.items():
        if j == times:
            return i * times
    return 0


# three_of_a_kind
# Four_of_a_kind
def three_of_a_kind(nums):
    return n_of_kind(nums, 3)


def four_of_a_kind(nums):
    return n_of_kind(nums, 4)


def full_house(nums):
    three = n_of_kind(nums, 3)
    two = n_of_kind(nums, 2)
    if three and two:
        return three + two
    else:
        return 0


def small_straight(nums):

    match_set = [[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]]
    if nums[:4] in match_set or nums[1:] in match_set:
        return 30
    return 0

def large_straight(nums):
    if nums in [[1, 2, 3, 4, 5], [2, 3, 4, 5, 6]]:
        return 40
    return 0

def yahtzee(nums):
    # use timeit to get what is the fastest method
    if len(set(nums)) == 1:
        return 50
    return 0


def chance(nums):
    return sum(nums)


def upper_section(nums):
    c = Counter(nums)
    temp = []
    for i in range(1, 7):
        try:
            temp.append(i * c[i])
        except KeyError:
            temp.append(0)
    return temp
