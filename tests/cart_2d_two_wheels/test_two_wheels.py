#
# test_two_wheels.py
#

import sys
sys.path.insert(0, '../../lib')

from models.cart2d import *
from models.robot import *
from gui.gui_2d import *

from PyQt5.QtWidgets import QApplication

class Cart2DRobot(RoboticSystem):

    def __init__(self):
        super().__init__(1e-3) # delta_t = 1e-3
        # Mass = 1kg
        # radius = 15cm
        # friction = 0.8
        # distance between traction wheels = 25cm
        self.cart = TwoWheelsCart2D(1, 0.15, 0.8, 0.8, 0.25)

    def run(self):
        self.cart.evaluate(self.delta_t, -0.45, 0.5)
        return True

    def get_pose(self):
        return (self.cart.x, self.cart.y, self.cart.theta)

    def get_speed(self):
        return (self.cart.v, self.cart.w)


if __name__ == '__main__':
    cart_robot = Cart2DRobot()
    app = QApplication(sys.argv)
    ex = CartWindow(cart_robot)
    sys.exit(app.exec_())
