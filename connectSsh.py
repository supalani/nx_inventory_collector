# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 23:39:04 2018

@author: suresh.palanisamy@nutanix.com
"""
#SSH module using paramiko
import paramiko
#-------------------------------------------------------------------------------
# Creating a constructor for SSH object from runInventory.py
class SSH:
# __init__ method where passing ssh server login arguments 
    def __init__(self, hostname, port, user, pasw):
        self.hostname = hostname
        self.port = port
        self.user = user
        self.pasw = pasw
#-------------------------------------------------------------------------------        
# A method where passing commands and returning back the cli output from ssh server         
    def sessionConnect(self, cmd_input):
        try:
            endPoint = paramiko.SSHClient()
            endPoint.load_system_host_keys()
            endPoint.set_missing_host_key_policy(paramiko.WarningPolicy)
            endPoint.connect(self.hostname, self.port, self.user, self.pasw)
            stdin, stdout, stderr = endPoint.exec_command(cmd_input)
            return stdout.read()
#        except:
#            return stdin.read()
            
        finally:
            endPoint.close()
#-------------------------------------------------------------------------------