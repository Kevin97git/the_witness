from multiprocessing import Pipe
a, b = Pipe()
x = [1, 2, 3]
a.send(x)
del x
print(b.recv())