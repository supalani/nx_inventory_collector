# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 21:18:06 2018

@author: suresh.palanisamy@nutanix.com
"""
#importing regex module
import re
#-------------------------------------------------------------------------------
# A class for fetching the commanOutput file and
# collecting few particular strings as inventory through methods - TrimData and
# noTrimData.
# TrimData collects particular data using regex
# noTrimData() collects exact data what was produced through 
# main module runInventory > commandExecution()
class DataQuery:    
    def __init__(self, commandOutput):
        self.commandOutput = commandOutput
#-------------------------------------------------------------------------------        
    def noTrimData(self):
        commandOutput = open(self.commandOutput, 'r')
        noTrim_dict = {}
        for readLine in commandOutput:
            if 'Network controller' in readLine:
                nic = 'NIC Model'
                split_nic = list(readLine.split())   
                join_nic = ' '.join(split_nic)
                add_label_1 = str('NIC Model\t: ') + str(join_nic)
                noTrim_dict[add_label_1] = nic
            if 'cpuModel =' in readLine:
                cpuModel = 'CPU Modle'
                split_cpumodel = list(readLine.split())
                split_cpumodel = [i for i in split_cpumodel if i not in ('cpuModel', '=')]
                split_cpumodel_1 = []
                for i in split_cpumodel:
                    i = re.sub(r'"', '', i)
                    i = re.sub(r',', '', i)
                    split_cpumodel_1.append(i)
                join_cpumodel = ' '.join(split_cpumodel_1)
                add_label_2 = str('CPU Model\t: ') + str(join_cpumodel)
                noTrim_dict[add_label_2] = cpuModel
            if '/dev/sd' in readLine:
                drive = 'Drive Model'
                split_drive = list(readLine.split())
                join_drive = ' '.join(split_drive)
                add_label_3 = str('Drive Model\t: ') + str(join_drive)
                noTrim_dict[add_label_3] = drive
            if '/dev/disks/t10' in readLine:
                boot_device = 'Boot Device'
                split_boot = list(readLine.split())
                join_boot = ' '.join(split_boot)
                add_label_4 = str('Boot Device\t: ') + str(join_boot)
                noTrim_dict[add_label_4] = boot_device
        commandOutput.close()
        sort_noTrim_dict = sorted(noTrim_dict)
        return sort_noTrim_dict
#-------------------------------------------------------------------------------    
    def trimData(self):
        commandOutput = open(self.commandOutput, 'r')
        Trim_list = []
        readFile = commandOutput.read()
        bios_match = re.search(r'(BIOS Version)\.+(\w+.\w)', readFile)
        if bios_match:
            Trim_list.append(bios_match.group(1) + '\t' + ': ' + bios_match.group(2))
        mac_match = re.search(r'(MAC Address)\s+:(.+)', readFile)
        if mac_match:
            Trim_list.append(mac_match.group(1) + '\t' + ':' + mac_match.group(2))
        bmc_match = re.search(r'(BMC Version).+(\w+.\w+)', readFile)
        if bios_match:
            Trim_list.append(bmc_match.group(1) + '\t' + ': ' + bmc_match.group(2))
        memory_match = re.search(r'(Physical Memory):\s(\d+)', readFile)
        if memory_match:
            byte_conv = lambda x : ((int(x) / 1024) / 1024 ) / 1024
            byte_to_gb =  byte_conv(memory_match.group(2))
            Trim_list.append(memory_match.group(1) + '\t' + ': ' + str(byte_to_gb) + ' GB')       
        cpu_core_match = re.search(r'(CPU Cores):.(\d+)', readFile)
        if cpu_core_match:
            Trim_list.append(cpu_core_match.group(1) + '\t' + ': ' + cpu_core_match.group(2))
        commandOutput.close()
        return Trim_list
#-------------------------------------------------------------------------------            

            
    
