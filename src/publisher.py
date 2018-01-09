import socket
import time
import rospy
import os
import json
import thread
import udpnode
from DirectorNode.msg import Order
from barrieduino.srv import *

UDP_IP = "127.0.0.1"
UDP_PORT = 5006
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

def setup_publisher():
  global pub
  pub = rospy.Publisher('orders', Order, queue_size=10)

def publish_message(message):
  global pub
  pub.publish(message)

def handle_msg(msg):
  if msg.split(':')[0] == 'order':
      print Order(msg.split(':')[1])
      publish_message(Order(msg.split(':')[1]))
  elif msg.split(':')[0] == 'stock':
      column = msg.split(':')[1]
      stock = get_stock(column) # TODO right stock (add parameter to srv call)
      udpnode.send_stock(column, stock)

def get_stock(column):
    rospy.wait_for_service('/sensors')
    try:
        stock_srv = rospy.ServiceProxy('/sensors', sensorRequestResponse)
        stock_srv(column)
        return
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def recv_data():
  while not rospy.is_shutdown():
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print "received message:", data

def start():
  setup_publisher();
  thread.start_new_thread(recv_data, ())
