#!/usr/bin/env python
import socket
import time
import rospy
import os
import json
from kt.msg import point
from kt.msg import Cursor
from std_msgs.msg import Int32
from std_msgs.msg import UInt32

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

# //define the display text
def cursors_callback(data):
  rospy.loginfo("I receive %s", data.cursors)
  sock.sendto(build_points_packet(data.cursors), (UDP_IP, UDP_PORT))
  sock.sendto(build_points_packet(data.cursors), (UDP_IP, UDP_PORT+1))

def states_callback(data):
  rospy.loginfo("I receive state change: %s", data.data)
  sock.sendto(build_state_packet(data.data), (UDP_IP, UDP_PORT))
  sock.sendto(build_state_packet(data.data), (UDP_IP, UDP_PORT+1))

def rfid_callback(data):
  rospy.loginfo("I receive rfid id: %s", data.data)
  sock.sendto(build_rfid_packet(data.data), (UDP_IP, UDP_PORT))
  sock.sendto(build_rfid_packet(data.data), (UDP_IP, UDP_PORT+1))

def build_rfid_packet(rfid_id):
  data = {}
  data['rfid'] = rfid_id
  return json.dumps(data)

def build_points_packet(points):
  data = {}
  p = []
  for point in points:
      p.append((point.x, point.y))
    #   print((point.x, point.y))
    #   print('-----')
  data['cursors'] = p
  return json.dumps(data)

def build_state_packet(state):
  data = {}
  data['state'] = state
  return json.dumps(data)

def random_subscriber():
  rospy.init_node('udpnode')
  rospy.Subscriber('kinect_touch',Cursor, cursors_callback)
  rospy.Subscriber('states', Int32, states_callback)
  rospy.Subscriber('RFID', UInt32, rfid_callback)
  rospy.spin()

if __name__=='__main__':
  random_subscriber()
