# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 13:08:22 2020

@author: Vasantha Kumar
"""
'''
Purpose:
    This script will open every whatsapp contact and
    saves the DP in a user given folder.
    
Pre-requisities:
    It is better to enable 'airplane mode' to avoid distractions.
    
    It is mandatory to keep the mobile in 'portrait mode'.
    
    It is mandatory to open the required WhatsAPP app,
    if more than one versions of WhatsAPP are installed in the mobile. 
    
    It is mandatory that SD card needs to be mounted in the mobile.
    
    It is mandatory to disable the lock feature of PC and mobile.

Tested:
    This script is tested on Android10 mobile.   
    
Profile:
    For 18 contacts, the execution takes 9 to 10 minutes 
    in consecutive executions.
        
'''

# START OF CODE

# import necessary standard packages
import os, cv2, pytesseract, time
import numpy as np
from PIL import Image

# import library functions
import General
from General import Lib


'''
The following variables need to be given by the user
'''
# assign the mobile device id. User to give.
device_id       = "Z9IZT8P74DQC6LBA"

# assign the foldername in which the DP pictures need to be saved
new_img_folder  = "new"

# assign the path where Tesseract exe is present in the PC
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# assign sdcard name
sdcard_name = "/storage/6533-3034/"

# flag to indicate WhatsAPP is opened by user or not
# 0 -> This scriiot will open the app
# give this, when there is only one instance of WhatsAPP in the mobile
# 1 -> The user opened the WhatsAPP
# give this, when more than one instances of WhatsAPP are present in the mobile
# open the app which needs to be processed
app_opened = 1


class DPSaver(Lib):
    
    # initiate the width of the screen
    ScreenWidth     = 0
    
    # initiate the height of the screen
    ScreenHeight    = 0
    
    # initiates the group icon variable
    GroupiconCount  = 0    
    
    # initiates diff variable
    imgDiff = 0
    
    # initiates an image buffer across functions
    imAfter = []

    '''
    Function        : MoveToFullTop
    Purpose         : To scroll up WhatsAPP app until it reaches the top
    Functinality    : By comparing the screenshots of the previous and scrolled up screens
    Arguments       : None
    Return          : RETURN CODES      
    '''
                
    def MoveToFullTop(self):
        
        global device_id, sdcard_name
        
        try:
            
            comp_y_start_pt = int(0.478632 * self.ScreenHeight)
            comp_y_end_pt   = int(0.521367 *self.ScreenHeight)
            
            swipe_x_st_pt   = int(0.462963  * self.ScreenWidth)
            swipe_y_st_pt   = int(0.34188   * self.ScreenHeight)
            swipe_y_end_pt  = int(0.6410256 * self.ScreenHeight)
            
            crop_pt_three   = 0
            crop_pt_four    = int(self.ScreenWidth - 10)
            
            while 1:        
                
                # Capture mobile screen and save the image in test PC
                self.SaveScreenshotOnPC(device_id, sdcard_name, "Project", ".", "InitialScreen.png")
                
                # Read the saved the image using OpenCV
                imRef = cv2.imread("./InitialScreen.png")
                
                # Convert to grayscale for comparison
                gray = cv2.cvtColor(imRef, cv2.COLOR_BGR2GRAY)
                
                # Crop the middle segment of the image        
                CropImgRef = gray[comp_y_start_pt:comp_y_end_pt, 
                                  crop_pt_three:crop_pt_four]
                
                # scroll up the screen
                self.ApplySwipe(device_id, 
                               swipe_x_st_pt, swipe_y_st_pt, 
                               swipe_x_st_pt, swipe_y_end_pt, 
                               "Just swipe")            
                
                time.sleep(2)
                
                # Capture mobile screen and save the image in test PC
                self.SaveScreenshotOnPC(device_id, sdcard_name, "Project", ".", "ScrollScreen.png")
                
                # Read the saved the image using OpenCV
                im1 = cv2.imread("./ScrollScreen.png")
                
                # Convert to grayscale for comparison
                gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)       
                
                # Crop the middle segment of the image
                CropImg = gray[comp_y_start_pt:comp_y_end_pt, 
                               crop_pt_three:crop_pt_four]
                
                # Compare the two cropped segments
                imgDiff = cv2.absdiff(CropImg, CropImgRef)        
                
                # if both the segments same then the scroll operation
                # doesn't change the screen. It means the screen reaches bottom
                # Break the while loop        
                if not np.any(imgDiff):
                    break
            
            return General.SUCCESS_CODE
            
        except Exception as e:
            
            self.log_file_write("Exception :"+str(e)+". Moving to Full top of the screen : FAILED.") 
            
            return General.ERROR_CODE 
        
    '''
    Function        : InitiateWhatsapp
    Purpose         : To open an instance of whatsAPP
    Functinality    : By using adb call 
    Arguments       : None
    Return          : RETURN CODES    
    '''    
    
    def InitiateWhatsapp(self):
        
        global device_id
        
        adb_cmd_open_whatsapp ="adb -s "+device_id+" shell am start -n com.whatsapp/com.whatsapp.Main"
        
        os.system(adb_cmd_open_whatsapp)
        
        return Lib.SUCCESS_CODE

    '''
    Function        : Common
    Purpose         : Common function called in two different scenarios
    Functinality    : By using adb call 
    Arguments       : tap point
    Return          : RETURN CODES    
    '''     
    
    def Common(self, tap_point):
        
        global device_id, sdcard_name
        
        scrn_half_width = int(self.ScreenWidth/2)
        
        tap_point_two   = int(0.0641 * self.ScreenHeight)
        
        crop_pt_one     = int(0.478632 * self.ScreenHeight)
        crop_pt_two     = int(0.521367 * self.ScreenHeight)
        crop_pt_three   = 0
        crop_pt_four    = int(self.ScreenWidth - 10)
        
        dp_pic_pt       = int(0.149572 * self.ScreenHeight)
        
        time.sleep(2)
        self.ApplyTap(device_id, scrn_half_width, tap_point, 'Tap on contact')
        time.sleep(2)
        
        self.ApplyTap(device_id, scrn_half_width, tap_point_two, 'Tap on contact')
        time.sleep(2)
        self.SaveScreenshotOnPC(device_id, sdcard_name, "Project", ".", "BeforeTapContactImage.png")
        
        imBefore = cv2.imread("./BeforeTapContactImage.png")
        gray = cv2.cvtColor(imBefore, cv2.COLOR_BGR2GRAY)
        CropImgBefore = gray[crop_pt_one:crop_pt_two, crop_pt_three:crop_pt_four]
        
        self.ApplyTap(device_id, scrn_half_width, dp_pic_pt, 'Tap on contact')
        time.sleep(5)
        self.SaveScreenshotOnPC(device_id, sdcard_name, "Project", ".", "AfterTapContactImage.png")
                    
        self.imAfter = cv2.imread("./AfterTapContactImage.png")
        gray = cv2.cvtColor(self.imAfter, cv2.COLOR_BGR2GRAY)
        CropImgAfter = gray[crop_pt_one:crop_pt_two, crop_pt_three:crop_pt_four]
        
        self.imgDiff = cv2.absdiff(CropImgBefore, CropImgAfter)    
        
        return General.SUCCESS_CODE

    '''
    Function        : Process
    Purpose         : Main function in which the complete process runs
    Functinality    : By using adb calls 
    Arguments       : None
    Return          : RETURN CODES    
    '''          
    
    def Process(self):
        
        global device_id, new_img_folder, sdcard_name
        
        try:
            # Finds the resolution of the device
            self.ScreenWidth, self.ScreenHeight = self.GetDeviceResolution(device_id)
            self.ScreenWidth     = int(self.ScreenWidth)
            self.ScreenHeight    = int(self.ScreenHeight)
            
            tap_point_one   = int(0.213675 * self.ScreenHeight)
            
            scrn_half_width = int(self.ScreenWidth/2)
            
            crop_pt_one     = int(0.478632 * self.ScreenHeight)
            crop_pt_two     = int(0.521367 * self.ScreenHeight)
            crop_pt_three   = 0
            crop_pt_four    = int(self.ScreenWidth - 10)
            
            dp_pic_crop_pt_one = int(0.294117 * self.ScreenHeight)
            dp_pic_crop_pt_two = int(0.743697 * self.ScreenHeight)
            
            contact_name_pt_one     = int(0.0641   * self.ScreenHeight)
            contact_name_pt_two     = int(0.094017 * self.ScreenHeight)
            contact_name_pt_three   = int(0.120370 * self.ScreenWidth)
            contact_name_pt_four    = int(0.879629 * self.ScreenWidth)
            
            swipe_pt_one    = int(0.299145 * self.ScreenHeight)
            swipe_pt_two    = int(0.245726 * self.ScreenHeight)
            swipe_pt_three  = int(0.75641  * self.ScreenHeight)
            
            initial_row_inc = int(0.1068376 * self.ScreenHeight)
            
            # moves the screen to the top of whatsAPP
            self.MoveToFullTop()        
            
            while 1:            
                
                self.Common(tap_point_one)
                
                if np.any(self.imgDiff):
        
                    CropImgContactName = self.imAfter[contact_name_pt_one:contact_name_pt_two, 
                                      contact_name_pt_three:contact_name_pt_four]
    
                    cv2.imwrite("name.png",CropImgContactName)    
                    imagename = "name.png"                
                    ContactName = pytesseract.image_to_string(Image.open(imagename))
                    FullName = ContactName[0:len(ContactName)-2]  
                    
                    if FullName == "Group icon":                
                        FullName = "Groupicon_" + str(self.GroupiconCount)
                        self.GroupiconCount = self.GroupiconCount + 1
        
                    print(FullName)
                    self.contacts_log_file_write("***Contact Name Found for : "+FullName+"***")
                    CropImgContact = self.imAfter[dp_pic_crop_pt_one:dp_pic_crop_pt_two, crop_pt_three:crop_pt_four]
                    imgname = new_img_folder+"/"+FullName + "__DPContact.png"
                    cv2.imwrite(imgname, CropImgContact)    
                
                    
                    for i in range(3):
                        self.ExecuteBackCommand(device_id)
                else:
                    for i in range(2):
                        self.ExecuteBackCommand(device_id)
         
        
                self.SaveScreenshotOnPC(device_id, sdcard_name, "Project", ".", "BeforeSwipe.png")
                imBefore = cv2.imread("./BeforeSwipe.png")
                gray = cv2.cvtColor(imBefore, cv2.COLOR_BGR2GRAY)
                CropImageBeforeSwipe = gray[crop_pt_one:crop_pt_two, crop_pt_three:crop_pt_four]
                
                self.ApplySwipe(device_id, scrn_half_width, swipe_pt_one, 
                               scrn_half_width, swipe_pt_two, 
                               "Just swipe")
                time.sleep(2)        
                                        
                
                self.SaveScreenshotOnPC(device_id, sdcard_name, "Project", ".", "AfterSwipe.png")
                imAfter = cv2.imread("./AfterSwipe.png")
                gray = cv2.cvtColor(imAfter, cv2.COLOR_BGR2GRAY)
                CropImageAfterSwipe = gray[crop_pt_one:crop_pt_two, crop_pt_three:crop_pt_four]
                
                imgDiff = cv2.absdiff(CropImageBeforeSwipe, CropImageAfterSwipe)   
                
                if np.any(imgDiff):
                    continue
                else:
                    break
                
            initial_row = swipe_pt_one
            
            # the count 6 is based on the remaining contacts
            # once the app reaches the bottom
            for i in range(6):
                
                self.Common(initial_row)
                
                if np.any(self.imgDiff):
                    
                    CropImgContactName = self.imAfter[contact_name_pt_one:contact_name_pt_two, 
                                      contact_name_pt_three:contact_name_pt_four]
                    cv2.imwrite("name.png",CropImgContactName)    
                    imagename = "name.png" 
                    ContactName = pytesseract.image_to_string(Image.open(imagename))
                    FullName = ContactName[0:len(ContactName)-2]
                    
                    if FullName == "Group icon":                
                        FullName = "Groupicon_" + str(self.GroupiconCount)
                        self.GroupiconCount = self.GroupiconCount + 1
                    
                    print(FullName)
                    self.contacts_log_file_write("***Contact Name Found for : "+FullName+"***")
                    CropImgContact = self.imAfter[swipe_pt_one:swipe_pt_three, 
                                         crop_pt_three:crop_pt_four]
                    
                    imgname = new_img_folder+"/"+FullName + "__DPContact.png"
                    cv2.imwrite(imgname, CropImgContact)    
                
                    
                    for i in range(3):
                        self.ExecuteBackCommand(device_id)
                else:
                    for i in range(2):
                        self.ExecuteBackCommand(device_id)
                
                initial_row = initial_row + initial_row_inc
                        
                        
            # deletes all the temporary images
            os.remove('AfterSwipe.png')
            os.remove('AfterTapContactImage.png')
            os.remove('BeforeSwipe.png')
            os.remove('BeforeTapContactImage.png')
            os.remove('name.png')
            
            # moves the app to the top
            self.MoveToFullTop()
            
            # deletes all the unwanted images
            os.remove('InitialScreen.png')
            os.remove('ScrollScreen.png')

            # calculates the time taken. Logged and Printed
            print('\n***Task Completed***\n')             
            
        except Exception as e:
            print('\n***Task Failed***\n')  
            self.log_file_write("Exception :"+str(e)+". The main process : FAILED.") 


# main call
if __name__ == "__main__":
    
       
    # assigns the start time of the process
    t0 = time.process_time()
    
    # prints the start time
    print('Welcome to Whatsapp DP Saver Tool')
    print('***Task Started***')    
    print('Start Time: ' + str(t0))        

    # assigns the DP folder with path
    new_img_folder = "./" + new_img_folder
    
    # creates an object
    obj = DPSaver()
    
    # checks whether the new images folder exists or not
    # if not, crates it
    if not os.path.exists(new_img_folder):
        obj.log_file_write("The new image folder doesn't exist.\n\
                           The new images folder will be created.\
                           The new images will be saved in new folder.")
        
        os.mkdir(new_img_folder)        
    
    if app_opened == 0:
        obj.InitiateWhatsapp()
        
    obj.Process()
       
    t1 = time.process_time()
    print('End Time: ' + str(t1))
    print('Total time taken: '+str(t1-t0))
     
        
# END OF CODE
        
