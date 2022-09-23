# Modified by SparkFun Electronics June 2021
# Author: Wes Furuya
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warrranty of
# MERCHANABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/license>
#
#==================================================================================
# Copyright (c) 2021 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#==================================================================================

import time
import traitlets
from traitlets.config.configurable import SingletonConfigurable
#import qwiic
import RPi.GPIO as GPIO
#from .motor import Motor
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
# Scan for devices on I2C bus

class Robot():


	def __init__(self, *args, **kwargs):
		super(Robot, self).__init__(*args, **kwargs)

		self.left_motor = [35,36]
		self.right_motor = [37,38]
#		print(self.left_motor, self.right_motor)
		self.left_speed = 0
		self.right_speed = 0
		GPIO.setup(32,GPIO.OUT)
		GPIO.setup(33,GPIO.OUT) 
		self.pwm=[GPIO.PWM(32,50),GPIO.PWM(33,50)]
		GPIO.setup(self.left_motor[0],GPIO.OUT,initial=GPIO.LOW)
		GPIO.setup(self.right_motor[0],GPIO.OUT,initial=GPIO.LOW) 
		GPIO.setup(self.left_motor[1],GPIO.OUT,initial=GPIO.LOW)
		GPIO.setup(self.right_motor[1],GPIO.OUT,initial=GPIO.LOW) 
		self.pwm[0].start(0)
		self.pwm[1].start(0)

	def set_motors(self, left_speed, right_speed):
		GPIO.output(self.left_motor[0],GPIO.HIGH)
		GPIO.output(self.right_motor[0],GPIO.HIGH) 
		self.left_speed = ((left_speed - (-1))/2)*100
		self.right_speed = ((right_speed - (-1))/2)*100
		print()
		print()
		self.pwm[0].ChangeDutyCycle(self.left_speed)
		self.pwm[1].ChangeDutyCycle(self.right_speed)

	def _right(self, speed=1.0, duration=None):
		GPIO.output(self.left_motor[0],GPIO.HIGH)
		GPIO.output(self.right_motor[0],GPIO.HIGH) 
		GPIO.output(self.left_motor[1],GPIO.LOW)
		GPIO.output(self.right_motor[1],GPIO.LOW) 
		self.speed = ((speed - (-1))/2)*100
		self.pwm[0].ChangeDutyCycle(self.speed)
		self.pwm[1].ChangeDutyCycle(self.speed)

	def _left(self, speed=1.0):
		GPIO.output(self.left_motor[0],GPIO.LOW)
		GPIO.output(self.right_motor[0],GPIO.LOW) 
		GPIO.output(self.left_motor[1],GPIO.HIGH)
		GPIO.output(self.right_motor[1],GPIO.HIGH) 
		self.speed = ((speed - (-1))/2)*100
		self.pwm[0].ChangeDutyCycle(self.speed)
		self.pwm[1].ChangeDutyCycle(self.speed)

	def _backward(self, speed=1.0):
		GPIO.output(self.left_motor[0],GPIO.LOW)
		GPIO.output(self.right_motor[0],GPIO.HIGH) 
		GPIO.output(self.left_motor[1],GPIO.HIGH)
		GPIO.output(self.right_motor[1],GPIO.LOW) 
		self.speed = ((speed - (-1))/2)*100
		self.pwm[0].ChangeDutyCycle(self.speed)
		self.pwm[1].ChangeDutyCycle(self.speed)

	def _forward(self, speed=1.0):

		GPIO.output(self.left_motor[0],GPIO.HIGH)
		GPIO.output(self.right_motor[0],GPIO.LOW) 
		GPIO.output(self.left_motor[1],GPIO.LOW)
		GPIO.output(self.right_motor[1],GPIO.HIGH) 
		self.speed = ((speed - (-1))/2)*100
		self.pwm[0].ChangeDutyCycle(self.speed)
		self.pwm[1].ChangeDutyCycle(self.speed)

	def _stop(self):
		GPIO.output(self.left_motor[0],GPIO.LOW)
		GPIO.output(self.right_motor[0],GPIO.LOW) 
		GPIO.output(self.left_motor[1],GPIO.LOW)
		GPIO.output(self.right_motor[1],GPIO.LOW) 
		self.left_speed = 0
		self.right_speed = 0
		self.pwm[0].ChangeDutyCycle(self.left_speed)
		self.pwm[1].ChangeDutyCycle(self.right_speed)

	def wiggle(self):
		for _ in range(5):
			self._right()
			time.sleep(0.5)
			self._left()
			time.sleep(0.5)
			self._stop()

	def donut(self):
		self._right()
		time.sleep(4.6)
		self._stop()


	def shuffle(self):
		for _ in range(5):
			self._forward()
			time.sleep(0.5)
			self._backward()
			time.sleep(0.5)
			self._stop()

	def leftMoonwalk(self):
		self._left()
		time.sleep(1)
		for _ in range(3):
			self._backward()
			time.sleep(0.5)
			self._stop()
			time.sleep(0.3)

	def rightMoonwalk(self):
		self._right()
		time.sleep(1)
		for _ in range(3):
			self._backward()
			time.sleep(0.5)
			self._stop()
			time.sleep(0.3)

	def right(self, speed=1):
		self._right()
		time.sleep(speed)
		self._stop()
	def left(self, speed=1):
		self._left()
		time.sleep(speed)
		self._stop()
	def backward(self, speed=1):
		self._backward()
		time.sleep(speed)
		self._stop()
	def forward(self, speed=1):
		self._forward()
		time.sleep(speed)
		self._stop()
	def stop(self):
		self._stop()
		#time.sleep(0.1)
		#self._stop()
