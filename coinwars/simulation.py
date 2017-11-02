from .game import Game

def print_coins(coins):
    for i, coin in enumerate(coins):
        print(i, repr(coin))
    print()

gg = Game()
s1 = gg.get_simulation()
s2 = gg.get_simulation()

s1_c1 = s1.simulation.table.coins[0]
s1_c2 = s1.simulation.table.coins[8]
s1.simulation.shoot_coin(s1_c1, target=s1_c2)

s2_c1 = s2.simulation.table.coins[4]
s2_c2 = s2.simulation.table.coins[6]
s2.simulation.shoot_coin(s2_c1, target=s2_c2)

while gg.table.tick():
    pass

while s1.simulation.table.tick():
    pass

while s2.simulation.table.tick():
    pass

print("gg")
print_coins(gg.table.coins)
print("s1")
print_coins(s1.simulation.table.coins)
print("s2")
print_coins(s2.simulation.table.coins)
