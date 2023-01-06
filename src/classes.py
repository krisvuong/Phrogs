import random
import copy


class Creature:
    def __init__(self):
        self.name = "unnamed creature"
        self.damage = 1
        self.health = 1
        self.tier = 1
        self.level = 1
        self.num = 0

    def attack(self, other):
        return other.health - self.damage

    def change_health(self, x):
        if self.health + x <= 0:
            return 1
        return self.health + x

    def change_damage(self, x):
        if self.damage + x <= 0:
            return 1
        return self.damage + x


class Item:
    def __init__(self):
        self.name = "food"
        self.damage = 0
        self.health = 0


class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self, pos):
        return self.items.pop(pos)

    def size(self):
        return len(self.items)

    def peek(self):
        return self.items[-1]

    def look(self, pos):
        return self.items[pos]


# Each player (2) will be an object of the Player class
class Player:
    def __init__(self):
        self.team = [0, 0, 0, 0, 0]  # Contains creatures on user's team
        # self.items = [0, 0, 0, 0, 0]  # Contains items on user's team
        self.coins = 10  # Used to purchase creatures/items; resets every round
        self.lives = 10  # Decreases if round is lost; game over at 0 lives
        self.wins = 0  # Increases for every round won
        self.creature_shop = []
        self.item_shop = []

    # Adds a creature to the player's team
    def buy_creature(self, creature, position):
        # Check if at least 3 coins
        # Check if position is empty (no other creature already there)
        if self.team[position] == 0:
            self.coins -= 3
            self.team[position] = copy.deepcopy(creature)

    # Remove a creature from the player's team
    def sell_creature(self, pos):
        # Check if position is not empty
        if self.team[pos] != 0:
            self.coins += int(self.team[pos].level)  # Number of coins gained = level of creature sold
            self.team[pos] = 0  # Remove creature from list

    # Swap position of two animals on the player's team
    def change_pos(self, pos, dir):
        # First (left-most) animal cannot move left
        if pos == 0 and dir == -1:
            return
        # Last animal (right-most) cannot move right
        elif pos == 4 and dir == 1:
            return
        # Only valid case: middle animals move left or right
        else:
            self.team[pos], self.team[pos + dir] = self.team[pos + dir], self.team[pos]


class Game:
    def __init__(self, player_1, player_2):
        self.all_creatures = []  # Contains ALL creatures in the game
        self.all_items = []  # Contains ALL items in the game
        self.team = [0, 0, 0, 0, 0]  # Contains creatures on user's team
        self.items = [0, 0, 0, 0, 0]  # Contains items on user's team
        self.coins = 10  # Used to purchase creatures/items; resets every round
        self.lives = 10  # Decreases if round is lost; game over at 0 lives
        self.wins = 0  # Increases for every round won
        self.turns = 1  # Increases for every round played
        self.creature_shop = []
        self.item_shop = []
        self.player_1 = player_1
        self.player_2 = player_2

    def read_creatures(self, fname):
        file_in = open(
            fname, 'r',
            encoding='utf-8-sig')  # encoding option fixes formatting
        lines = file_in.readlines(
        )  # Read all lines of text file, save as list of long strings

        count = 0  # Counter to represent line number in text file
        for i in lines:
            single_line = i[0:-1].split(", ")  # Make copy of each line
            temp = Creature(
            )  # Create creature object using temporary variable
            temp.name = single_line[0]  # Assign attributes
            temp.damage = int(single_line[1])
            temp.health = int(single_line[2])
            temp.tier = single_line[3]
            temp.num = count  # Unique line number relates to each creature
            count += 1  # Increase line number
            self.all_creatures.append(
                temp)  # Append all class objects to a list
        file_in.close()

    def read_items(self, fname):
        file_in = open(
            fname, 'r',
            encoding='utf-8-sig')  # encoding option fixes formatting

        lines = file_in.readlines()  # Read all lines of text file, save as list of long strings

        count = 0
        for i in lines:
            single_line = i[0:-1].split(", ")  # Make copy of each line
            temp = Item()
            temp.name = single_line[0]
            temp.damage = int(single_line[1])
            temp.health = int(single_line[2])
            self.all_items.append(temp)

        file_in.close()  # Close text file

    def load_shop(self, player, first_run):
        # Check if player has at least 1 coin
        if first_run:
            player.coins = 10
        if player.coins <= 0:
            return
        elif not first_run:
            player.coins -= 1

        num_creatures = 3  # Number of animals to display in shop
        num_items = 2  # Number of items to display in the shop

        # Empty creature and item shop
        self.creature_shop = []
        self.item_shop = []

        for _ in range(num_creatures):  # Append appropriate number of creatures to shop display
            self.creature_shop.append(random.choice(self.all_creatures[:(self.turns*8)]))
        for _ in range(num_items):
            self.item_shop.append(random.choice(self.all_items))

    def end_turn(self, team_1,
                 team_2):  # End of item shop (goes to battle sequence)
        player_1 = Queue()  # Create queue for player's team
        player_2 = Queue()  # Create queue for enemy team

        # Change list (of creature objects) to a Queue
        for i in range(len(team_1)):  # Iterate through team
            # LATER: NEED TO MAKE A SEPERATE FOR LOOP SO THAT BOTH TEAMS ARENT IDENTICAL
            a = copy.deepcopy(team_1[i])  # Copy so the objects aren't the same
            if a != 0:  # Getting rid of empty spots for the battle sequence
                player_1.enqueue(a)  #® Queue of player creature objects

        for i in range(len(team_2)):  # Iterate through team
            # LATER: NEED TO MAKE A SEPERATE FOR LOOP SO THAT BOTH TEAMS ARENT IDENTICAL
            b = copy.deepcopy(team_2[i])  # Copy so the objects aren't the same
            if b != 0:  # Getting rid of empty spots for the battle sequence
                player_2.enqueue(b)  # Queue of player creature objects

        # Call battle sequence with player and enemy teams
        return player_1, player_2

    # One creature does damage to another creature's health
    def attack(self, other):
        other.health -= self.damage

    # Battle sequence loop (first creature in each Queue fight until one Queue is empty)
    def battle(self, queue_1, queue_2):
        while not queue_1.is_empty or not queue_2.is_empty(
        ):  # While both teams have creatures still alive

            # Remove life from losing team
            if queue_1.is_empty():
                self.player_2.wins += 1
                self.player_1.lives -= 1
                break
            elif queue_2.is_empty():
                self.player_1.wins += 1
                self.player_2.lives -= 1
                break

            # Creatures attack each other
            queue_1.peek().attack(queue_2.peek())
            queue_2.peek().attack(queue_1.peek())

            # Remove fainted creatures (if health <= 0)
            if queue_1.peek().health <= 0:  # If a creature faints, remove it
                queue_1.dequeue()  # Next creature moves to the front
            if queue_2.peek().health <= 0:
                queue_2.dequeue()
