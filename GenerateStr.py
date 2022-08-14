import random

def GenStr(number):
    str = ""
    i = 0
    while i < number:
        possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        str = str + possible[random.randint(0, len(possible)-1)]
        i = i + 1
    return str
