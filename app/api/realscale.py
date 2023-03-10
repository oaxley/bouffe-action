# -*- coding: utf-8 -*-
# vim: filetype=python
#
# This source file is subject to the Apache License 2.0
# that is bundled with this package in the file LICENSE.txt.
# It is also available through the Internet at this address:
# https://opensource.org/licenses/Apache-2.0
#
# @author	Alex Colson
# @license	Apache License 2.0
#
# @brief	Interface for interacting with the scale
#----- imports

import app.config as config
from . import api, create_response
from flask import abort
import serial
from serial.tools import list_ports
import threading
import queue

import time

SERIAL_SPEED = 9600
import logging

def singleton(class_):
    instances = {}
    locking = threading.Lock()
    def getinstance(*args, **kwargs):
        with locking:
            if class_ not in instances:
                instances[class_] = class_(*args, **kwargs)
            return instances[class_]
    return getinstance

@singleton
class ScaleInterface():
    def __init__(self):
        self.alive = True
        self.responses = queue.Queue()
        self.events = queue.Queue()
        self._event_thread = threading.Thread(target=self.even_loop)
        self._event_thread.daemon = True
        self._event_thread.name = 'scale-interface'
        self.ser : serial.Serial = None

        # state variables
        self.weight : float = 0.0
        self.stable : bool = False
        self.has_value : bool = False
        self.is_serial_ready : bool = False        

        self.lock = threading.Lock()

        self._event_thread.start()



    def stop(self):
        """
        Stop the event processing thread, abort pending commands, if any.
        """
        self.alive = False
        self._event_thread.join()

    def reset_scale(self):
        with self.lock:
            self.weight = None
            self.stable = False
            self.has_value = False
            self.is_serial_ready = False

    def even_loop(self)-> None:
        while self.alive:
            if not self.has_serial():
                if self.is_serial_ready:
                    self.reset_scale()
                time.sleep(1)
                continue
            else:
                if not self.is_serial_ready:
                    self.init_serial_connection()
            
            if not self.ser.inWaiting():
                # nothing to read
                time.sleep(0.5)
                continue
            last_line = self.ser.readlines()[-1]
            last_line = last_line.strip()
            # should have format like
            # ASNG/W+  0.00  kg
            status_str = last_line[:7]
            (_, stable, has_error) = status_str[:3]
            with self.lock:
                if stable == "S":
                    self.stable = True
                else:
                    self.stable = False
                self.has_value = True
                self.weight = float(last_line.split()[1])

    def init_serial_connection(self):
        with self.lock:
            ports = list_ports.comports()
            port_name = ports[0].device
            print(f"Initializing com on port={port_name}/{SERIAL_SPEED}")
            self.ser = serial.Serial(port_name, SERIAL_SPEED)
            self.is_serial_ready = True
            print(f"SUCESS Initializing com on port={port_name}/{SERIAL_SPEED}")

    def scale_ready(self)->bool:
        return self.has_serial() and self.has_value

    def has_serial(self) -> bool:
        return len(list_ports.comports()) > 0

    def get_reading(self):
        with self.lock:
            return (self.stable, self.weight)

SI = None
if not SI:
    SI = ScaleInterface()

def get_scale():
    global SI
    if not SI.scale_ready():
        if not SI.has_serial():
            abort(config.HTTP_NOT_FOUND, "No Com port detected")
        else:
            abort(config.HTTP_NOT_FOUND, "No data")            
    else:
        (stable, weight) = SI.get_reading()
        res = {'value':round(weight,2), 'stable': stable}
        return create_response(res, config.HTTP_OK)


