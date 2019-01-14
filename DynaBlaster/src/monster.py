class Monster(object):

    def __init__(self, name, x, y):

        self.name = name
        self.pos_x = x
        self.pos_y = y

        self.isDead = False


    def move(self, x, y):

        self.pos_x = x
        self.pos_y = y

    def get_pos_x(self):

        return self.pos_x

    def get_pos_y(self):

        return self.pos_y

    def destroy(self):

        self.pos_x = -1
        self.pos_y = -1
