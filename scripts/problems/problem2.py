# In this challenge, the user enters a string and a substring. You have to print the number of times that the substring occurs in the given string. String traversal will take place from left to right, not from right to left.
#
#
def count_substring(string, sub_string):
    count = 0
    lastIndex = string.find(sub_string, 0, len(string))
    while lastIndex != -1:
        count += 1
        lastIndex = string.find(sub_string, lastIndex + 1, len(string))
    return count