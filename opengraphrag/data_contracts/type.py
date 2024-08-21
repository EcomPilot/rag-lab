from enum import IntEnum

class Strategy(IntEnum):
    fast = 0
    accuracy = 1


if __name__ == "__main__":
    print(Strategy.fast, Strategy.accuracy)