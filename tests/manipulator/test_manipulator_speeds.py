#
# test_manipulator_speeds.py
#

import sys
sys.path.insert(0, '../../lib')

from models.manipulator import *
from models.robot import *
from models.inputs import *
from controllers.standard import *
from data.plot import *
from gui.three_joints_gui import *

from PyQt5.QtWidgets import QApplication

class ManipulatorRobot(RoboticSystem):

    def __init__(self):
        super().__init__(1e-3) # delta_t = 1e-3
        self.arm = ThreeJointsPlanarArm(0.2, 0.2, 0.02,
                                        0.5, 0.5, 0.5,
                                        0.8)

        # joint 1
        self.speed_control_1 = PIDSat(400, 100, 0,
                                        20, True) # 20Nm max torque, antiwindup

        # joint 2
        self.speed_control_2 = PIDSat(400, 100, 0,
                                        20, True) # 20Nm max torque, antiwindup

        # joint 3
        self.speed_control_3 = PIDSat(10, 4, 0,
                                        20, True) # 20Nm max torque, antiwindup

        self.ramp = RampSat(2, 2)
        self.plotter = DataPlotter()

    def run(self):

        wref = self.ramp.evaluate(self.delta_t)
        w = self.arm.element_1.w
        torque = self.speed_control_1.evaluate(self.delta_t, wref, w)

        # wref = self.ramp.evaluate(self.delta_t)
        # w = self.arm.element_2.w
        # torque = self.speed_control_2.evaluate(self.delta_t, wref, w)

        # wref = self.ramp.evaluate(self.delta_t)
        # w = self.arm.element_3.w
        # torque = self.speed_control_3.evaluate(self.delta_t, wref, w)

        self.arm.evaluate(self.delta_t, torque, 0, 0)

        self.plotter.add('Wref', wref)
        self.plotter.add('W', w)
        self.plotter.add('T', torque)
        self.plotter.add('t', self.t)

        if self.t > 4:
            self.plotter.plot( [ 't', 'Time' ],
                               [ [ 'Wref', 'omega-Ref'] , [ 'W', 'omega' ] ])
            self.plotter.plot( [ 't', 'Time' ],
                               [ [ 'T', 'Torque']  ])
            self.plotter.show()
            return False
        else:
            return True

    def get_joint_positions(self):
        return self.arm.get_joint_positions()

    def get_pose_degrees(self):
        return self.arm.get_pose_degrees()



if __name__ == '__main__':
    robot = ManipulatorRobot()
    app = QApplication(sys.argv)
    ex = ManipulatorWindow(robot)
    sys.exit(app.exec_())
