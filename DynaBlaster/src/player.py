
class Player(object):

    def __init__(self, name, x, y):

        self.name = name
        self.pos_x = x
        self.pos_y = y
        self.bombs = 1
        self.isDead = False
        self.numOfLives = 3
        self.points = 0

    def move(self, x, y):

        self.pos_x = x
        self.pos_y = y

    def get_pos_x(self):

        return self.pos_x

    def get_pos_y(self):

        return self.pos_y

    def place_bomb(self):

        if self.bombs >= 1:
            self.bombs -= 1
            return self.pos_x, self.pos_y
        else:
            return 0, 0

    def give_bomb(self):

        self.bombs += 1

    def destroy(self):

        self.pos_x = -1
        self.pos_y = -1
