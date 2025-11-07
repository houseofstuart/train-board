
class Queue:
    def __init__(self):
        self.queue = []
        self.head = -1
        self.tail = -1
    
    def enqueue(self, item):
        if(not item):
            print("Can't enqueue nothing")
            return
        if(len(self.queue) == 0): #first enqueue
            self.queue.append(item)
            self.head = 0
            self.tail = 0
        else:
            self.queue.append(item)
            self.tail += 1
        

    def dequeue(self):
        if(len(self.queue) == 0):
            print("Queue is empty")
            return
        dequeue = self.queue.pop(self.head)
        self.tail -= 1
        return dequeue


