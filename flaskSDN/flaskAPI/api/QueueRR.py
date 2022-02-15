class QueueRR:
    def __init__(self):
        self.dest_nodes = []

    def isEmpty(self):
        return self.dest_nodes == []

    def enqueue(self, item):
        self.dest_nodes.insert(0,item)

    def dequeue(self):
        return self.dest_nodes.pop()

    def size(self):
        return len(self.dest_nodes)

    def append_queue(self, item):
        self.dest_nodes.append(item)

