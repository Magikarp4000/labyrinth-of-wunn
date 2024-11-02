from collections import deque

class BFS:
    def __init__(self):
        # dictionary of position => (distance, from)
        self.res = {}

    def __call__(self, start):
        pass

    def impl_(self, graph, start):
        self.res.clear()
        q = deque([graph[start]])
        while q:
            node = q.popleft()
            for j in graph[node]:
                if j not in self.res:
                    self.res[j] = {self.res[node][0] + 1, node}
                    q.append(j)
