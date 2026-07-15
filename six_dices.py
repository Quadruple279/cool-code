import random
import time

#  Fucking Dices
#  ● ┌ ─ ┐ │ └ ┘

dices = {
    1: ("┌─────────┐",
        "│         │",
        "│    ●    │",
        "│         │",
        "└─────────┘"),
    2: ("┌─────────┐",
        "│    ●    │",
        "│         │",
        "│    ●    │",
        "└─────────┘"),
    3: ("┌─────────┐",
        "│      ●  │",
        "│    ●    │",
        "│  ●      │",
        "└─────────┘"),
    4: ("┌─────────┐",
        "│  ●   ●  │",
        "│         │",
        "│  ●   ●  │",
        "└─────────┘"),
    5: ("┌─────────┐",
        "│  ●   ●  │",
        "│    ●    │",
        "│  ●   ●  │",
        "└─────────┘"),
    6: ("┌─────────┐",
        "│  ●   ●  │",
        "│  ●   ●  │",
        "│  ●   ●  │",
        "└─────────┘")
}

print("DICE ROULETTE".center(100, "="))
print("")

track_rolls = []
for i in range(6):
    time.sleep(1)
    print(f"{6 - i} ROLL(S) LEFT".center(100, " "))

    roll = random.randint(1, 6)
    track_rolls.append(roll)

    for i in range(5):
        print(dices.get(roll)[i].center(100, " "))

time.sleep(1)


print(" SUMMARY".center(100, "-"))
print("")
print(f"TOTAL SCORE: {sum(track_rolls)}".center(100, " ") + "\n")


for i in range(5):
    print(f"{dices.get(track_rolls[0])[i]:^16} {dices.get(track_rolls[1])[i]:^16} {dices.get(track_rolls[2])[i]:^16} {dices.get(track_rolls[3])[i]:^16} {dices.get(track_rolls[4])[i]:^16} {dices.get(track_rolls[5])[i]:^16}")

print("")

if sum(track_rolls) < 20:
    print("Calamity strikes again.".center(100, " "))
else:
    print("Nice.".center(100, " "))