#!/usr/bin/env python
import socket
import time
import rospy
import os
import json
from kt.msg import point
from kt.msg import Cursor

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

# //define the display text
def callback(data):
  rospy.loginfo("I receive %s", data.cursors)
  sock.sendto(build_packet(data.cursors), (UDP_IP, UDP_PORT))

def build_packet(points):
  data = {}
  p = []
  for point in points:
      p.append((point.x, point.y))
    #   print((point.x, point.y))
    #   print('-----')
  data['cursors'] = p
  return json.dumps(data)

def random_subscriber():
  rospy.init_node('udpnode')
  rospy.Subscriber('chatter',Cursor, callback)
  rospy.spin()

if __name__=='__main__':
  random_subscriber()
