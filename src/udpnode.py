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
from director_node.msg import Order
import publisher
import numpy

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
    rospy.loginfo("I receive rfid id: %s", data.data)
    sock.sendto(build_rfid_packet(data.data), (UDP_IP, UDP_PORT))

def order_finished_callback(data):
    if (data.order_type == 255):
        rospy.loginfo("I receive order is finished")
        sock.sendto(build_ordercomplete_packet(), (UDP_IP, UDP_PORT))

def send_stock(column, value):
    sock.sendto(build_inventory_packet(column, value), (UDP_IP, UDP_PORT))

def build_ordercomplete_packet():
    data = {}
    data['order'] = True
    return json.dumps(data)

def build_inventory_packet(column, value):
    data = {}
    data['stock'] = column
    data['value'] = value
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
  rospy.Subscriber('RFID', UInt32, rfid_callback)
  rospy.Subscriber('finishedOrders', Order, order_finished_callback)

if __name__=='__main__':
  setup_subscriber()
  publisher.start()
  rospy.spin()
