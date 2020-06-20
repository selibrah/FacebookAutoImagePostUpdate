from selenium import webdriver
from time import sleep
import time
import pyperclip
import keyboard
from selenium.webdriver.common.keys import Keys
import pickle
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

# This Script Update A Facebook Post Every time te Reaction and Comments number


# Image Height and Width

MAX_W, MAX_H = 940, 788

# Text Image

font = ImageFont.truetype('fontf.ttf', 100)

# Chrome Setup

chrome_options = webdriver.ChromeOptions()

# Disable notifications and images and others options to make page load faster

#prefs = {"profile.default_content_setting_values.notifications" : 2}#,"profile.managed_default_content_settings.images": 2}
prefs = {'profile.default_content_setting_values': { 'images': 2,'plugins': 2, 'popups': 2, 'geolocation': 2, 
                            'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2, 
                            'mouselock': 2, 'mixed_script': 2, 'media_stream': 2, 
                            'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2, 
                            'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2, 
                            'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2, 
                            'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2, 
                            'durable_storage': 2}}
chrome_options.add_experimental_option("prefs",prefs)

# This line make the script run without opening the browser

chrome_options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options=chrome_options)

def waitf(selc, tim,typ):

    # faction to wait till the presence of element or the element to be clickable
    # Selc (By.CLASS_NAME,"_81hb")
    # tim Time to wait
    # typ presence or clickable

    wait = WebDriverWait(driver, tim)
    if typ == "presence":
        element = wait.until(ec.presence_of_element_located(selc))
    elif typ == "clickable":
        element = wait.until(ec.element_to_be_clickable(selc))
    return element

# Facebook Login page

def FBLogin():

    # Go FaceBook page
    
    driver.get("https://facebook.com")
    
    # Wait for login button appears

    waitf((By.XPATH,'//*[@id="u_0_b"]'), 6, "clickable")

    # Input your Email

    driver.find_element_by_xpath("//*[@id=\"email\"]")\
        .send_keys("elibrahimi.soufiane@gmail.com")

    # Input The PassWord
    
    driver.find_element_by_xpath("//*[@id=\"pass\"]")\
        .send_keys("Sibra161996**")
    # Click The login button
    driver.find_element_by_xpath('//*[@id="u_0_b"]')\
        .click()
def AddTextToImage(Current_React_Number, Current_Cmnt_Number):
    astr = "Had el post fih " + Current_React_Number + " React And " + Current_Cmnt_Number + " Cmnt."
    #astr = "This Post Has " + Current_React_Number + " Reactions And " + Current_Cmnt_Number + " Comments."
    para = textwrap.wrap(astr, width=15)
    image = Image.open("magic.png")
    draw = ImageDraw.Draw(image)
    current_h, pad = MAX_W / 4, 20
    for line in para:
        w, h = draw.textsize(line, font=font)
        draw.text(((MAX_W - w) / 2, current_h), line, font=font)
        current_h += h + pad
    image.save('magi.png')

# Login to Facebook

print("FBLogin")
FBLogin()
sleep(4)
try:
    mynm = waitf((By.XPATH,"//span[@class='_1vp5']"),10,"presence").text
    print(mynm)
except:
    print("login error")
    driver.save_screenshot("screenshoterror.png")


# Go to the post page

PostLink = "https://www.facebook.com/sofiane.elibrahimi/posts/1970298336447619"
print("go to post")

driver.get(PostLink)
#waitf((By.CLASS_NAME,"_81hb"),10,"presence")
sleep(4)

print("Start")
driver.save_screenshot("screenshot1.png")
print("# Start checking for Reactions or Comments number changes to update the post")

while(1):
    tim = time.time()
    try:

        #print("# Get old Reaction and comments from Saved File")

        with open('objs.pkl','rb') as f:  # Python 3: open(..., 'rb')
            Old_React_Number, Old_Cmnt_Number = pickle.load(f)
        try:

            #print("# Get the Current Reactions Number")
            
            Current_React_Number = waitf((By.CLASS_NAME,"_81hb"),10,"presence").text
            
            #print("# Get the Current Comments Number")
            
            CmntInfo = waitf((By.XPATH,"//a[@class='_3hg- _42ft']"),10,"presence").text
            Current_Cmnt_Number = (CmntInfo.split())[0]

        except Exception as e:
            print("Get Post Info Exception :")
            print(e)
            Current_React_Number = Old_React_Number
            Current_Cmnt_Number = Old_Cmnt_Number

        if Current_React_Number != Old_React_Number or Current_Cmnt_Number != Old_Cmnt_Number:

            print("# Start Updating The Post ")
            
            print("Go")
            tic = time.time()
            driver.get("https://m.facebook.com/sofiane.elibrahimi/posts/1970298336447619")
            waitf((By.XPATH,"//a[@class='_4s19 sec']"), 5, "clickable").click()
            waitf((By.XPATH,"//a[@class='_39pi']"), 5, "clickable").click()
            waitf((By.LINK_TEXT,"More Options"), 5, "clickable").click()
            waitf((By.LINK_TEXT,"Edit Photo"), 5, "clickable").click()
            waitf((By.LINK_TEXT,"Delete"), 5, "clickable").click()
            waitf((By.XPATH,"//button[@class='btn btnC mfss touchable']"), 5, "clickable").click()
            print("Deleted")
            driver.get("https://m.facebook.com/sofiane.elibrahimi/posts/1970298336447619")
            waitf((By.XPATH,"//a[@class='_4s19 sec']"), 5, "clickable").click()
            waitf((By.LINK_TEXT,"Add photos"), 5, "clickable").click()
            waitf((By.XPATH,"//button[@class='btn btnI bgb mfss touchable']"), 5, "presence")
            AddTextToImage(Current_React_Number, Current_Cmnt_Number)
            active_ele = driver.find_element_by_xpath("//input[@class='_5scc']")
            active_ele.send_keys(os.getcwd()+"/magi.png")
            waitf((By.XPATH,"//button[@class='btn btnI bgb mfss touchable']"), 5, "clickable").click()
            print(time.time() - tic)
            print("Posted")
            print("#Save old Reaction and comments from Saved File")
            driver.get(PostLink)
            sleep(3)
            with open('objs.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
                pickle.dump([Current_React_Number, Current_Cmnt_Number], f)

            print("#Remove Image")

            os.remove(os.getcwd()+"/magi.png")

    except Exception as e:
        print(e)
        print("errrorr")
        driver.get(PostLink)
        sleep(3)
