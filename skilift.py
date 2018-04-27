"""
Code for simulating a lift at a ski resort:

>>> num_benches = 10
>>> bench_class = Quad
>>> lift = Lift(num_benches, bench_class)
>>> line = Line(num_people=10)
>>> lift.simulate(line)
{'loaded': 10, 'unloaded': 10, 'num_benches': 8}
"""

from collections import deque


class Line:
    def __init__(self, num_people):
        self.num_people = num_people

    def take(self, amount):
        if amount > self.num_people:
            amount = self.num_people
        self.num_people -= amount
        return amount

    def add(self, amount):
        self.num_people += amount

    def __bool__(self):
        return bool(self.num_people)


class _Bench:
    size = 1
    def __init__(self, id):
        self.count = 0
        self.id = id
    def load(self, num):
        self.count += num
    def unload(self):
        val = self.count
        self.count = 0
        return val

    
class Quad(_Bench):
    size = 4


class Lift:
    def __init__(self, num_benches, bench_class):
        half = num_benches / 2
        self._up = deque()
        self._down = deque()
        for i in range(num_benches):
            if i < half:
                self._up.append(bench_class(i))
            else:
                self._down.append(bench_class(i))
        self.bench_size = bench_class.size

    def people_riding_up(self):
        return any(bench.count for bench in self._up)

    def simulate(self, line):
        results = {'loaded': 0, 'unloaded':0, 'num_benches':0}
        while line:
            self.one_bench(line, results)
        #get them to the top
        while self.people_riding_up():
            self.one_bench(line, results)
        return results

    def one_bench(self, line, results=None):
        results = results or {'loaded': 0, 'unloaded':0, 'num_benches':0}
        num = line.take(self.bench_size)
        # load bottom
        bench = self._down.popleft()
        bench.load(num)
        self._up.append(bench)
        results['loaded'] += num
        # unload top
        bench = self._up.popleft()
        num = bench.unload()
        results['unloaded'] += num
        self._down.append(bench)
        results['num_benches'] += 1
        return results

if __name__ == '__main__':
    import doctest
    doctest.testmod()
