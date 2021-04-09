class AlreadyUsedField(Exception):
    def __init__(self,message):
        self.message = message

class KeyNotAllowed(Exception):
    def __init__(self, message):
        self.message = message

class SequencesFinished(Exception):
    def __init__(self, message):
        self.message = message

class AllRoundsCompleted(Exception):
    def __init__(self, message):
        self.message = message