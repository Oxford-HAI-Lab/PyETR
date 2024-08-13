from pyetr.cases import e17

print(e17)

e17.test(verbose=True)

print(e17.v)  # ({~King(k())Ace(a()),King(k())~Ace(a())}, {King(k())})
print(e17.c)  # {~Ace(a())}
