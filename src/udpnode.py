#!/usr/bin/env python
import socket
import time
import rospy
import os
import json
import thread
from kt.msg import point
from kt.msg import Cursor
from std_msgs.msg import Int32
from std_msgs.msg import UInt32
from sensor_msgs.msg import Image
import publisher
from framedata import frame
import base64

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

# //define the display text
def cursors_callback(data):
  rospy.loginfo("I receive %s", data.cursors)
  sock.sendto(build_points_packet(data.cursors), (UDP_IP, UDP_PORT))

def states_callback(data):
  rospy.loginfo("I receive state change: %s", data.data)
  sock.sendto(build_state_packet(data.data), (UDP_IP, UDP_PORT))

def rfid_callback(data):
  rospy.loginfo("I receive height: %s", data.height)
  rospy.loginfo("I receive encoding: %s", data.encoding)
  base64EncodedStr = base64.b64encode(data.data)
  sock.sendto(build_frame_packet(base64EncodedStr), (UDP_IP, UDP_PORT))

def build_frame_packet(framedata):
    data = {}
    data['frame'] = framedata
    return json.dumps(data)

def build_rfid_packet(rfid_id):
  data = {}
  data['rfid'] = rfid_id
  return json.dumps(data)

def build_points_packet(points):
  data = {}
  p = []
  for point in points:
      p.append((point.x, point.y))
  data['cursors'] = p
  return json.dumps(data)

def build_state_packet(state):
  data = {}
  data['state'] = state
  return json.dumps(data)

def setup_subscriber():
  rospy.init_node('udpnode')
  rospy.Subscriber('kinect_touch',Cursor, cursors_callback)
  rospy.Subscriber('states', Int32, states_callback)
  rospy.Subscriber('/camera/depth/image_raw', Image, rfid_callback)

if __name__=='__main__':
  setup_subscriber()
  publisher.start()
  rospy.spin()
