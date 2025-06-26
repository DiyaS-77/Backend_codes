import dbus
import dbus.service
import dbus.mainloop.glib
import os
import subprocess
import time
from gi.repository import GObject
import mimetypes
from dbus.mainloop.glib import DBusGMainLoop



dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

class BluetoothDeviceManager:
    def __init__(self):
        self.bus = dbus.SystemBus()
        self.adapter_path = '/org/bluez/hci0'
        self.adapter_proxy = self.bus.get_object('org.bluez', self.adapter_path)
        self.adapter = dbus.Interface(self.adapter_proxy, 'org.bluez.Adapter1')
        self.adapter_proxy = self.bus.get_object('org.bluez',self.adapter_path)
        self.adapter = dbus.Interface(self.adapter_proxy, 'org.bluez.Adapter1')
        self.stream_process = None
        self.device_path = None
        self.device_address = None
        self.device_sink = None
        self.devices = {}
        self.last_session_path = None
        self.opp_process = None

    def start_discovery(self):
        """Function to start discovery"""
        self.adapter.StartDiscovery()

    def stop_discovery(self):
        """Function to stop discovery"""
        self.adapter.StopDiscovery()

    def inquiry(self,timeout):
        """Function for inquiry with inquiry timeout being mentioned"""
        self.start_discovery()
        time.sleep(timeout)
        self.stop_discovery()
        devices = []
        bus = dbus.SystemBus()
        om = dbus.Interface(bus.get_object("org.bluez", "/"), "org.freedesktop.DBus.ObjectManager")
        objects = om.GetManagedObjects()
        for path, interfaces in objects.items():
            if "org.bluez.Device1" in interfaces:
                devices.append(path)
        for device_path in devices:
            device = dbus.Interface(bus.get_object("org.bluez", device_path), dbus_interface="org.bluez.Device1")
            device_props = dbus.Interface(bus.get_object("org.bluez", device_path),dbus_interface="org.freedesktop.DBus.Properties")
            device_address = device_props.Get("org.bluez.Device1", "Address")
            print("Device Address")
            print(device_address)
            print("Device Name")
            device_name = device_props.Get("org.bluez.Device1", "Alias")
            print(device_name)
