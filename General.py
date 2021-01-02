# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 13:14:51 2020

@author: Vasantha Kumar
"""
import os
import datetime

#from datetime import *
#from time import *
import subprocess

from datetime import *
from time import *


SUCCESS_CODE        =  0
ERROR_CODE          = -1
CALL_FAILURE_CODE   = -2
WAIT_CODE           =  2

# declares script execution log file.
Exec_log_file_Name = "Exec_log_file.txt"

# declares contacts log file.
Contacts_log_file_Name = "Contacts.txt"

# assigns log file path to execution log file.
Exec_log_file = open(Exec_log_file_Name, "w")

# assigns log file path to contacts log file.
Contacts_log_file = open(Contacts_log_file_Name, "w")

# assigns task number. used for counting the tasks performed in the log file
TASK_NO = 1

# assigns contact number
Contact_NO = 1


class Lib:
    
    def log_file_write(self, msg):
        
        global TASK_NO, Exec_log_file
        
        Exec_log_file.write(str(TASK_NO)+"\t"+str(datetime.now())+"\t\t"+msg+"\n")
        Exec_log_file.flush()
        TASK_NO += 1
        return SUCCESS_CODE
    
    def contacts_log_file_write(self, msg):
        
        global Contact_NO, Contacts_log_file
        
        Contacts_log_file.write(str(Contact_NO)+"\t"+str(datetime.now())+"\t\t"+msg+"\n")
        Contacts_log_file.flush()
        Contact_NO += 1
        return SUCCESS_CODE    
    
    def GetDeviceResolution(self, device_id):
        try:
            cmd = "adb -s "+device_id+" shell wm size"
          
            self.log_file_write("Start Action:: SUCCESS : Getting Device Properties for Device with Device id: "+ device_id)
            dev_resolution_out = subprocess.check_output(cmd, shell=True)
            
            list_dev_res = dev_resolution_out.decode("utf-8").split(" ")[2].lstrip().rstrip().split("x")        
            self.log_file_write("End Action:: SUCCESS : Getting Device Properties for Device with Device id: "+ device_id+"\n")
            return list_dev_res
        except Exception as e:
            self.log_file_write("End Action:: FAILED : Getting Device Properties for Device with Device id: "+ device_id+"\n")
            self.log_file_write("Exception message: "+ str(e)+".\n")
            return ERROR_CODE
        
    def ApplySwipe(self, device_id, x_one, y_one, x_two, y_two, printable_text, duration_ms=100):
        adb_cmd_apply_swipe = "adb -s "+device_id+" shell input swipe "+str(x_one)+" "+str(y_one)+" "+str(x_two)+" "+str(y_two)+" "+str(duration_ms)
        try:
            self.log_file_write("Start Action:: SUCCESS : Applying swipe command on Device with Device id: "+ device_id +" from ("+str(x_one)
                           +" , "+str(y_one)+") to ("+str(x_two)+" , "+str(y_two)+") co-ordinates within "+str(duration_ms)+" ms time"+printable_text)
            os.system(adb_cmd_apply_swipe)
            self.log_file_write("End Action:: SUCCESS : Applying swipe command on Device with Device id: "+ device_id +" from ("+str(x_one)
                           +" , "+str(y_one)+") to ("+str(x_two)+" , "+str(y_two)+") co-ordinates within "+str(duration_ms)+" ms time"+printable_text+"\n")
    
            return SUCCESS_CODE
        except Exception as e:
            self.log_file_write("End Action:: FAILED : Applying swipe command on Device with Device id: "+ device_id +" from ("+str(x_one)
                           +" , "+str(y_one)+") to ("+str(x_two)+" , "+str(y_two)+") co-ordinates within "+str(duration_ms)+" ms time"+printable_text+"\n")
    
            self.log_file_write("Exception message: "+ str(e)+".\n")
            return ERROR_CODE
    
    
    def ApplyTap(self, device_id, x_pos, y_pos, printable_text):
        adb_cmd_apply_tap = "adb -s "+device_id+" shell input tap "+str(x_pos)+" "+str(y_pos)
        try:
            self.log_file_write("Start Action:: SUCCESS : Applying tap command on Device with Device id: "+ device_id +" at ("+str(x_pos)
                           +" , "+str(y_pos)+")"+printable_text)
            os.system(adb_cmd_apply_tap)
            self.log_file_write("End Action:: SUCCESS : Applying tap command on Device with Device id: "+ device_id +" at ("+str(x_pos)
                           +" , "+str(y_pos)+")"+printable_text+"\n")
    
            return SUCCESS_CODE
        except Exception as e:
            self.log_file_write("End Action:: FAILED : Applying tap command on Device with Device id: "+ device_id +" at ("+str(x_pos)
                           +" , "+str(y_pos)+")"+printable_text+"\n")
            self.log_file_write("Exception message: "+ str(e)+".\n")
            return ERROR_CODE    
    
    def SaveScreenshotOnPC(self, device_id, sdcard_name, img_folder_dut, img_folder_pc, file_name):
        ret_code = self.ScreenCaptureDevice(device_id, sdcard_name+img_folder_dut+"/"+file_name)
        if ret_code != SUCCESS_CODE:
            return ret_code
    
        ret_code = self.PullFilefromDev(device_id, sdcard_name+img_folder_dut+"/"+file_name, img_folder_pc)
        if ret_code != SUCCESS_CODE:
            return ret_code
    
        ret_code = self.DeleteFilesinDev(device_id, sdcard_name+img_folder_dut+"/"+file_name)
        if ret_code != SUCCESS_CODE:
            return ret_code
    
        return SUCCESS_CODE
    
    def ScreenCaptureDevice(self, device_id, directory_path):
        captures_screen_device = "adb -s "+device_id+" shell screencap -p "+directory_path
        try:
            self.log_file_write("Start Action:: SUCCESS : Captures screen on Device with Device id: "+ device_id+" in directory "+directory_path)
            os.system(captures_screen_device)
            self.log_file_write("End Action:: SUCCESS : Captures screen on Device with Device id: "+ device_id+" in directory "+directory_path+"\n")
            return SUCCESS_CODE
        except Exception as e:
            self.log_file_write("End Action:: FAILED : Captures screen on Device with Device id: "+ device_id+" in directory "+directory_path+"\n")
            self.log_file_write("Exception message: "+ str(e)+".\n")
            return ERROR_CODE
    
    def PullFilefromDev(self, device_id, dev_file_path, test_pc_directory_path):
        pull_file_dev = "adb -s "+device_id+" pull "+dev_file_path+" "+test_pc_directory_path
        try:
            self.log_file_write("Start Action:: SUCCESS : Pulls "+dev_file_path+" on Device with Device id: "+ device_id+" to directory "+test_pc_directory_path)
            os.system(pull_file_dev)
            self.log_file_write("End Action:: SUCCESS : Pulls "+dev_file_path+" on Device with Device id: "+ device_id+" to directory "+test_pc_directory_path+"\n")
            return SUCCESS_CODE
        except Exception as e:
            self.log_file_write("End Action:: FAILED : Pulls "+dev_file_path+" on Device with Device id: "+ device_id+" to directory "+test_pc_directory_path+"\n")
            self.log_file_write("Exception message: "+ str(e)+".\n")
            return ERROR_CODE
    
    def DeleteFilesinDev(self, device_id, directory_path):
        clears_log_device = "adb -s "+device_id+" shell rm -r "+ directory_path
        try:
            self.log_file_write("Start Action:: SUCCESS : Deletes all the files on Device with Device id: "+ device_id+" in directory "+directory_path)
            os.system(clears_log_device)
            self.log_file_write("End Action:: SUCCESS : Deletes all the files on Device with Device id: "+ device_id+" in directory "+directory_path+"\n")
            return SUCCESS_CODE
        except Exception as e:
            self.log_file_write("End Action:: FAILED : Deletes all the files on Device with Device id: "+ device_id+" in directory "+directory_path+"\n")
            self.log_file_write("Exception message: "+ str(e)+".\n")
            return ERROR_CODE
    
    def ExecuteBackCommand(self, device_id):
        adb_cmd_device_back = "adb -s "+device_id+" shell input keyevent KEYCODE_BACK"
        try:
            self.log_file_write("Start Action:: SUCCESS : Back command on Device with Device id: "+ device_id)
            os.system(adb_cmd_device_back)
            self.log_file_write("End Action:: SUCCESS : Back command on Device with Device id: "+ device_id+"\n")
            return SUCCESS_CODE
        except Exception as e:
            self.log_file_write("End Action:: FAILED : Back command on Device with Device id: "+ device_id+"\n")
            self.log_file_write("Exception message: "+ str(e)+".\n")
            return ERROR_CODE        
        
        