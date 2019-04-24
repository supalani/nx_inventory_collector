# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 07:48:53 2018

@author: suresh.palanisamy@nutanix.com
"""
#importing user defind ssh module
import connectSsh # User-defined module
import searchData # User-defined module
import os
import sys
#-------------------------------------------------------------------------------
# Script for collecting inventory info such as Platform Model, CPU Model,
# CPU Cores and threads, Memory capacity, NIC, SSD or HDD or NVMe
#-------------------------------------------------------------------------------
# This variable is decalard in global.
# This ipmi will be provided in command line and passed as part of IPMI command in commandSet()
ipmi =''
#-------------------------------------------------------------------------------
# A method where orginating all required commands to get the inventory
def commandSet():
    global ipmi
    ipmi_command_base = 'ipmitool -I lanplus -H ' + ipmi + '-U ADMIN -P ADMIN '
    ipmi_command_fru = ipmi_command_base + 'fru'
    ipmi_command_lan = ipmi_command_base + 'lan print'
    cmd = {ipmi_command_fru : 'IPMI', 
           ipmi_command_lan : 'IPMI',
           'lspci | grep Network' : 'ESX',
           'esxcli hardware memory get' : 'ESX',
           'esxcli hardware cpu global get' : 'ESX',
           'esxcfg-info -w | grep "BIOS Version"' : 'ESX',
           'esxcfg-info -w | grep "BMC"' : 'ESX',
           'vim-cmd hostsvc/hostsummary | grep cpuModel' : 'ESX',
           'fdisk -l' : 'ESX',
           '/usr/local/nutanix/cluster/bin/list_disks' : 'CVM'}
    return cmd
#-------------------------------------------------------------------------------
# A method where storing the output of commands as a file
def commandResult(a):
    createFile = open('commandOutput.txt', 'a+')
    createFile.write(a)
    createFile.close()
#-------------------------------------------------------------------------------
#1 A method where passing foundation, host and cvm login tuples
# to module : connectSSH > method : SSH
#2 Iterating the commands in module : connectSSH > method : sessionConnect
#3 Passing output of commands to method : collectData for creating a file
def commandExecution():
    global ipmi
    user = 'nutanix'
    password = 'nutanix/4u'
    host_user = 'root'
    port = 22
    if len(sys.argv) != 5:
        print 'Script usage: runInventory.py <foundation IP> <ESX host IP> <CVM IP>'
        sys.exit(1)
    fvm = sys.argv[1]
    ipmi = sys.argv[2]
    hvm = sys.argv[3]
    cvm = sys.argv[4]
    foundation_vm = connectSsh.SSH(fvm, port, user, password)
    esx_host = connectSsh.SSH(hvm, port, host_user, password)
    cvm = connectSsh.SSH(cvm, port, user, password)
    command = commandSet()
    for i in command:
        if command[i] == 'IPMI':
            output = foundation_vm.sessionConnect(i)
            commandResult(output) 
        if command[i] == 'ESX':
            output = esx_host.sessionConnect(i)
            commandResult(output)
        if command[i] == 'CVM':
            output = cvm.sessionConnect(i)
            commandResult(output)
#-------------------------------------------------------------------------------
#1 A method where the file is passsed as an argument into module searchData > method __init__
#2 calling two methods TrimData() and noTrimData() to display the inventory collection
#3 deleting the file what was created in method > commandResult()           
def dataAlign():
    passCommandOutput = searchData.DataQuery('commandOutput.txt')
    trimData = passCommandOutput.trimData()
    noTrimData = passCommandOutput.noTrimData()
    for i in trimData:
        print i
    for i in noTrimData:
        print i
    os.remove('commandOutput.txt')
#-------------------------------------------------------------------------------
# Overiding main() by assiging '__main__' and calling commandExecution() and dataAlign()
# for running whole script
if __name__ == '__main__':
    commandExecution()
    dataAlign()
#-------------------------------------------------------------------------------