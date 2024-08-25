from enum import Enum

class Strategy(Enum):
    ''' We have tow startegy for the RAG workflow.
    - fast
    - accuracy
    '''
    fast = 'fast'
    accuracy = 'accuracy'


if __name__ == "__main__":
    print(Strategy.fast, Strategy.accuracy)