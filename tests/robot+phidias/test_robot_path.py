#
# test_robot_path.py
#

import sys
sys.path.insert(0, '../../lib')

from models.cart2d import *
from models.robot import *
from controllers.standard import *
from controllers.control2d import *
from gui.gui_2d import *
from data.plot import *

from phidias.phidias_interface import *

from PyQt5.QtWidgets import QApplication

class Cart2DRobot(RoboticSystem):

    def __init__(self):
        super().__init__(1e-3) # delta_t = 1e-3
        # Mass = 1kg
        # radius = 15cm
        # friction = 0.8
        self.cart = Cart2D(1, 0.15, 0.8, 0.8)
        self.linear_speed_controller = PIDSat(10, 3.5, 0, 5) # 5 newton
        self.angular_speed_controller = PIDSat(6, 10, 0, 4) # 4 newton * metro
        self.polar_controller = Polar2DController(2.5, 2, 2.0 , 2)
        self.path_controller = Path2D(1.5, 2, 2, 0.01) # tolerance 1cm
        self.path_controller.set_path( [ (0.0, 0.0) ] )
        (x, y, _) = self.get_pose()
        self.path_controller.start( (x,y) )
        self.target_reached = False
        self.source_agent = ''
        start_message_server_http(self)

    def run(self):
        pose = self.get_pose()
        target = self.path_controller.evaluate(self.delta_t, pose)
        if target is not None:
            (x_target, y_target) = target
            (v_target, w_target) = self.polar_controller.evaluate(self.delta_t, x_target, y_target, self.get_pose())
            Force = self.linear_speed_controller.evaluate(self.delta_t, v_target, self.cart.v)
            Torque = self.angular_speed_controller.evaluate(self.delta_t, w_target, self.cart.w)
            self.cart.evaluate(self.delta_t, Force, Torque)
        else:
            if not(self.target_reached):
                self.target_reached = True
                if self.source_agent != '':
                    print("Target")
                    Messaging.send_belief(self.source_agent,'target_reached',[],'robot')
        return True

    def get_pose(self):
        return self.cart.get_pose()

    def get_speed(self):
        return (self.cart.v, self.cart.w)

    def on_belief(self, _from, name, terms):
        print(_from, name, terms)
        self.source_agent = _from
        if name == 'go_to':
            self.path_controller.set_path( [ (terms[0], terms[1]) ] )
            (x, y, _) = self.get_pose()
            self.path_controller.start( (x,y) )
            self.target_reached = False


if __name__ == '__main__':
    cart_robot = Cart2DRobot()
    app = QApplication(sys.argv)
    ex = CartWindow(cart_robot)
    sys.exit(app.exec_())
