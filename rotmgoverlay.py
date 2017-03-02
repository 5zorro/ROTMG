#! /usr/bin/env python
"""rotmgoverlay.py"""

import time
import os
import logging
#from PIL import Image #, ImageChops, ImageStat

import pyautogui
##
##  This is my program to create an auto game overlay for rotmg
##  The various functions are defined at the beginning, and they are
##  called at the end
#SETTING UP LOGGING
if os.path.isfile('ROTMGProgramLog.txt'):#this will delete what was in the logging file
    LOG = open('ROTMGProgramLog.txt', 'w')
    LOG.write('')
    LOG.close()
    
logging.basicConfig(
    filename='ROTMGProgramLog.txt',
    level=logging.DEBUG,
    format=' %(asctime)s - %(levelname)s - %(message)s')

logging.disable(level=logging.DEBUG) # this will disable DEBUG logging and
# slightly increase the speed of the program
logging.info('Start of program')

#SETTING UP FAILSAFES
pyautogui.PAUSE = .00 # wait 1.5 seconds after each function call.
#(user input or just waiting, but mostly just waiting)
pyautogui.FAILSAFE = True
#pyautogui.FailSafeException

#I had a Win 5 error when clicking, but it would still click, so this will bypass the error
def click_fix(button="left"):
    '''Bypass the Win Permission Error'''
    try:
        pyautogui.click(button=button)
    except PermissionError:
        pass

# create Game Overlay in the CMD Console
def update_console_overlay(game, where, count):
    '''Clear and update the Console's game overlay'''
    logging.info("Update GAME OVERLAY")
    logging.debug("clear the overlay")
    os.system('cls')
    print('Click on this Overlay and Press Ctrl-C to quit.')

    status = ' GameStatus: ' + game.rjust(7) + '\n'
    status += '  RealmName: ' + where.rjust(7) + '\n'
    status += 'AutoNexused: ' + str(count).rjust(7) + '\n'

    print(status, end='\n')

    global __updateOnNextRun__
    __updateOnNextRun__ = False

    logging.debug("finished printing the overlay")

def open_rotmg(xmousescale, ymousescale):
    '''Click on tray icons and drag around to start ROTMG'''

    global __steamIsClosed__
    global __gameStatus__
    global __updateOnNextRun__

    logging.info("opening Up ROTMG")
    steam_tray_loc = search_png("SteamTrayIcon", center=True)
    pyautogui.moveTo(steam_tray_loc[0]*xmousescale, steam_tray_loc[1]*ymousescale)
    click_fix("right")
    time.sleep(2/3)
    steam_tray_loc = search_png("ROTMGDropdown", center=True)
    #region = (trayLoc[0] - 200, trayLoc[1]+30, 50,100) )
    if steam_tray_loc is None:
        logging.error("trayloc must not be None" + str(steam_tray_loc)+ "screenshot created")
        pyautogui.screenshot("DebugScreenshot.png")
    pyautogui.moveTo(steam_tray_loc[0]*xmousescale, steam_tray_loc[1]*ymousescale)
    click_fix("left")
    logging.debug("ROTMG is coming into focus")
    time.sleep(7.5)
    rotmg_tray_loc = search_png("ROTMGTrayIconOpen")
    if rotmg_tray_loc is None:
        logging.debug("steam should be opening, this could take a while")
        time.sleep(60)
        rotmg_tray_loc = search_png("ROTMGTrayIconOpen")
    if rotmg_tray_loc is None:
        logging.error("Where is the rotmg Window?")
        pyautogui.screenshot("DebugScreenshot.png")
        raise Exception("ROTMG is unable to open")
    if rotmg_tray_loc is not None:
        logging.debug("ROTMG is open")
        #pyautogui.moveTo(a[0]*xmousescale,a[2]*ymousescale)
        #pyautogui.click()
        #time.sleep(5)
        #logging.debug("Just clicked on the ROTMG Tray. The window should be focused (green)")
    title_loc = search_png("ROTMGTitleGreen")
    if title_loc is None:
        logging.error("where is the ROTMG TITLE?")
        pyautogui.screenshot("DebugScreenshot.png")
        raise Exception("where is the ROTMG TITLE?")

    pyautogui.moveTo((title_loc[0]+title_loc[2])*xmousescale,
                     (title_loc[1]+title_loc[3])*ymousescale)
    #pyautogui.click(title_loc[0]*xmousescale,title_loc[1]*ymousescale)
    #time.sleep(2)
    try:
        pyautogui.mouseDown()
    except PermissionError:
        pass
    pyautogui.moveTo(50, 60)
    try:
        pyautogui.mouseUp()
    except PermissionError:
        pass

    __steamIsClosed__ = False
    __gameStatus__ = "Running"
    __updateOnNextRun__ = True
    time.sleep(.5)

def pixel_iteration(direction, allowable_px, working_location, screenshot):
    """iterate in various directions to when the pixels change"""
    print("iterating to the " + direction + " edge of the window")
    if direction == "top":
        direction = (1, -1) #affects the y variable (1) and goes up or (-1)
    if direction == "bottom":
        direction = (1, -1) #affects the y variable (1) and goes down or (1)
    if direction == "left":
        direction = (0, -1) #affects the x variable (0) and goes left or (-1)
    if direction == "right":
        direction = (0, 1) #affects the x variable (0) and goes right or (1)

    current_pixel = screenshot.load()[working_location[0], working_location[1]]
    x_size, y_size = pyautogui.size()
    if working_location[0] > x_size or working_location[1] > y_size:
        return

    while (current_pixel == screenshot.load()[working_location[0], working_location[1]]):
        working_location[direction[0]] += direction[1]
        if working_location[0] == x_size or working_location[1] == y_size:
            break
    pixel = ()
    for pixel in allowable_px:
        if pixel == screenshot.load()[working_location[0], working_location[1]]:
            return working_location

    working_location[direction[0]] += -direction[1]
    return working_location

#finds the corners of the ROTMG window to increase pixel searching efficiency
def update_rotmg_window_edges():
    """Find pixel area to search in and update vars"""
    logging.info("finding the ROTMG Window edges")

    allowable_pixel = [(119, 156, 72),
                       (130, 163, 88)]

    # print(px[0,1]) # yields (119,156,72) which is the main green
    # print(px[1,1]) # yields (119,156,72) which is the main green
    # print(px[1,0]) # yields (130,163,88) which is the lighter green

    screenshot = pyautogui.screenshot()

    pretitle_loc = search_png("greenTitleBar")
    if pretitle_loc is None:
        return None

    left_mid_pre = (pretitle_loc[0]-pretitle_loc[2]/2,
                    pretitle_loc[1],
                    pretitle_loc[2],
                    pretitle_loc[3])
    print("leftmost of the searched image ", left_mid_pre)
    # f = pyautogui.screenshot("debug.png", leftmostPre)
    #f.show()

    #iterate to the top pixel that matches
    top_left_loc = list(left_mid_pre[0:2])
    top_left_loc = pixel_iteration("top", allowable_pixel, top_left_loc, screenshot)
    top_left_loc = pixel_iteration("left", allowable_pixel, top_left_loc, screenshot)
    bottom_right_loc = pixel_iteration("right", allowable_pixel, top_left_loc, screenshot)
    bottom_right_loc = pixel_iteration("bottom", allowable_pixel, bottom_right_loc, screenshot)

    logging.debug(str(top_left_loc))
    logging.debug(str(bottom_right_loc))

    width, height = [a_i - b_i for a_i, b_i in zip(bottom_right_loc, top_left_loc)]
    return (top_left_loc[0], top_left_loc[1], width, height)

def search_png(file_root_str, region=None, center=False):
    """will search the directory this is stored in for PNGs like the root"""
    if center is False:
        #there is a specified region tuple (x,y,xwidth,yheight)
        for filename in os.listdir():
            if len(filename) < len(file_root_str) + 4:
                continue
            if filename[-4:] != ".png":
                continue
            if filename[:len(file_root_str)] == file_root_str:
                loc = pyautogui.locateOnScreen(filename, region=region)
                if loc is not None:
                    logging.info(filename + " matches PX on screen")
                    return loc
    else: #they want the Loc to be a center tuple of length (x,y)
        for filename in os.listdir():
            if len(filename) < len(file_root_str) + 4:
                continue
            if filename[-4:] != ".png":
                continue
            if filename[:len(file_root_str)] == file_root_str:
                loc = pyautogui.locateCenterOnScreen(filename, region=region)
                if loc is not None:
                    logging.info(filename + " matches PX on screen")
                    return loc

def update_where_vars(region=None):
    """Search for pngs to find where variables"""
    logging.info("Updating Where Vars")
    check_start_time = time.time()
    global __whereLoc__
    global __whereStr__
    global __whereIMG__
    logging.debug("beginning searches")
    __whereLoc__ = None
    if __whereLoc__ is None:
        __whereLoc__ = search_png("InARealm", region=region)
    if __whereLoc__ is not None:
        __whereStr__ = "Realm"
        __whereIMG__ = pyautogui.screenshot(region=__whereLoc__)
        logging.info("it took " + str(time.time()-check_start_time) + " seconds to find.")
        return
    if __whereLoc__ is None:
        __whereLoc__ = search_png("InNexus", region=region)
    if __whereLoc__ is not None:
        __whereStr__ = "Nexus"
        __whereIMG__ = pyautogui.screenshot(region=__whereLoc__)
        logging.info("it took " + str(time.time()-check_start_time) + " seconds to find.")
        return
    if __whereLoc__ is None:
        __whereStr__ = "Unknown"
        logging.info("it took " +
                     str(time.time()-check_start_time) +
                     " seconds to finish searches.")

def auto_nexuser():
    """will efficiently check the HP pixel to see if it is bad"""
    global __whereLoc__
    global __whereIMG__ #.load()
    global __whereStr__
    global __winLoc__
    global __HPBar__
    global __BAD_HP_PX__
    global __NEXUS_PERCENT__
    global __autoNexusCount__

    logging.debug(
        "this is if the whereloc equals the whereIMG" +
        str(pyautogui.locateOnScreen(__whereIMG__)) +
        str(__whereLoc__))
    # logging.debug("is whereIMG the same size as WhereLoc?" + str(whereIMG.size != whereLoc))
    # if whereIMG.size != whereLoc: update_where_vars()

    # logging.debug(     "If this is 0,0,0 then the two images are the same"+ '\n'+
    #     str(ImageChops.difference(whereIMG, pyautogui.screenshot(region = whereLoc)))+ '\n'+
    #     str(sum(ImageStat.Stat(ImageChops.difference(
    #           whereIMG, pyautogui.screenshot(region = whereLoc))).var))
    #     )

    logging.info("running autonexus ops")

    check_start_time = time.time()
    check_count = 0
    logging.debug("alternative image comparison " +
                  str(__whereIMG__ == pyautogui.screenshot(region=__whereLoc__))
                 )

    #the autonexuser needs to hve HPBar be an address
    if __HPBar__[0] == 0:
        initial_hp_loc = pyautogui.locateOnScreen("BeginningOfhpBar.png", region=__winLoc__)
        if initial_hp_loc is not None:
            x_coordinate, y_coordinate = initial_hp_loc[0:2]
            __HPBar__[0] = x_coordinate
            __HPBar__[1] = y_coordinate
        else:
            logging.critical("WHERE IS THE hp BAR? I made a screenshot")
            print("WHERE IS THE hp BAR? I made a screenshot")
            pyautogui.screenshot("DebugScreenshot.png")
    hp_loc = (__HPBar__[0] + __HPBar__[2]*__NEXUS_PERCENT__, __HPBar__[1] + .5*__HPBar__[3], 1, 1)

    nexus_image = __whereIMG__.convert(mode="1") #to make checking this more efficient
    #                               will be greyscale and cropped
    while nexus_image == pyautogui.screenshot(region=__whereLoc__).convert(mode="1"):
        #Reporting what is being done
        check_count += 1
        if (time.time() - check_start_time) >= 60:
            logging.info("Checked the hp " + str(check_count) + " times last minute.")
            print("Checked the hp " + str(check_count) + " times last minute.", end='\r')
            check_count = 0
            check_start_time = time.time()

        #this will send you to the nexus if you have selected the
        #ROTMG window
        #print("the value of b is" + str(b))
        im_pixel = pyautogui.screenshot(region=hp_loc).getpixel((0, 0))
        logging.debug("current value of hppixel is" + str(im_pixel))

        pixel = ()
        for pixel in __BAD_HP_PX__:
            if im_pixel == pixel:
                # then your health should be under 20 percent
                logging.debug("bad hp pixel is" + str(im_pixel))
                pyautogui.typewrite(["r", "enter", "r"])
                time.sleep(1)
                __autoNexusCount__ += 1
                logging.debug("Just nexused for the " + str(__autoNexusCount__) + " time(s)")
                return

        #if (impx == badhpPixelRGB) or (impx == badhpPixelRGB2):

    __whereStr__ = "JustTeleported"

# PLANNED FEATURE create a web scraper that determines from the wiki what projectiles
# damages are for whatever dungeon

# PLANNED FEATURE create a midlands fame train-esque guy
# who is able to identify and call candylands

# PLANNED FEATURE automate the fametrain

X_SIZE, Y_SIZE = pyautogui.size()
__updateOnNextRun__ = True
__steamIsClosed__ = True
__X_SCALE__ = X_SIZE/1920
__Y_SCALE__ = Y_SIZE/1080
__NEXUS_PERCENT__ = .20
__GOOD_HP_PX__ = [(197, 45, 45),
                  (224, 52, 52),
                  (213, 54, 54)]
__BAD_HP_PX__ = [(73, 73, 73),
                 (84, 84, 84)]
__HPBar__ = [0, 0, 219, 18] #begin pixel x,y and x width and y height
#im = pyautogui.screenshot()
__gameStatus__ = "Closed"
__autoNexusCount__ = 0
__winLoc__ = None
__whereStr__ = "Unknown"
__whereLoc__ = None
__whereIMG__ = None




#### BEGINNING OF MASTER FILE
def main():
    '''run ROTMG, Nexuser, and other features'''
    try:
        #setting up global variables
        global __X_SCALE__
        global __Y_SCALE__
        global __winLoc__
        global __HPBar__
        global __updateOnNextRun__
        global __whereStr__
        global __gameStatus__
        global __autoNexusCount__

        # This is the constant series of instructions
        open_rotmg(__X_SCALE__, __Y_SCALE__)
        __winLoc__ = update_rotmg_window_edges()
        window_image = pyautogui.screenshot(region=(__winLoc__[0], __winLoc__[1], 30, 30))
        window_image = window_image.convert(mode="1")
        while True:

            # if the ROTMG WINDOW has moved, update its edges
            if (window_image != pyautogui.screenshot(region=(__winLoc__[0], __winLoc__[1], 30, 30))
                    .convert(mode="1")):
                __winLoc__ = update_rotmg_window_edges()
                if __winLoc__ is None:
                    logging.info("The ROTMG window is no longer in focus")
                    print("The ROTMG window is no longer in focus")
                    # if the ROTMG window is closed, break from this while loop
                    break
                else:
                    #the rotmg window is in focus, but has moved.
                    #Update Images and Locs that are dependent on that
                    window_image = pyautogui.screenshot(
                        region=(__winLoc__[0], __winLoc__[1], 30, 30)
                        ).convert(mode="1")
                    __HPBar__[0:2] = 0, 0
                    __updateOnNextRun__ = True

            #set up the CMD Overlay if it needs to be updated
            if __updateOnNextRun__:
                update_console_overlay(__gameStatus__, __whereStr__, __autoNexusCount__)


            # EnterARealm.png refers to the picture you pick when you click enter.
            #to map this to a key like T or Y if i figure out how to make a
            # keylogger of this kind of prog.

            old_where_str = __whereStr__
            update_where_vars(__winLoc__) #update vars
            if __whereStr__ != old_where_str:
                __updateOnNextRun__ = True
                continue

            if __whereStr__ == "Realm":
                auto_nexuser()
                __updateOnNextRun__ = True

            #PLANNED FEATURE if I am in the nexus, I want to constantly check
            # for "FULL" and the mouse position
            # then autoclick like crazy until the whereIMG picture changes.
            if __whereStr__ == "Nexus":
                continue

    except KeyboardInterrupt:
        print('\nDone.')
        logging.debug('End of program')
    #except FailSafeException:
    #    print('\nDone.')
    #### END OF MASTER FILE
if __name__ == "__main__":
    main()
