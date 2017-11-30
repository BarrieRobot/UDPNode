import socket
import time
import rospy
import os
import json
import thread
from std_msgs.msg import String

UDP_IP = "127.0.0.1"
UDP_PORT = 5006
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

def setup_publisher():
  rospy.Publisher('chatter', String, queue_size=10)

def recv_data():
  while not rospy.is_shutdown():
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print "received message:", data

def start():
  setup_publisher();
  thread.start_new_thread(recv_data, ())
