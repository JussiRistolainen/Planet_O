from equations import Equations


class Sun(Equations):

    def __init__(self, screen, position_x, position_y, radius, density, classification, zoom):
        super(Sun, self).__init__(screen, radius, density, classification, position_x, position_y, zoom)

