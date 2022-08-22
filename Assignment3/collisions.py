class Collision:
    def __init__(self):
        self.count=0

    def increment(self):
        self.count+=1

    def decrement(self):
        self.count-=1

    def no_senders_currently_sending(self):
        return self.count
