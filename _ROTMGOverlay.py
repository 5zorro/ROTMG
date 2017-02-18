#! python3
# ROTMGMasterFile.py
import pyautogui,time, os
from PIL import Image #, ImageChops, ImageStat
import logging
##
##  This is my program to create an auto game overlay for rotmg
##  The various functions are defined at the beginning, and they are
##  called at the end
#SETTING UP LOGGING
if os.path.isfile('ROTMGProgramLog.txt'):#this will delete what was in the logging file
    f = open('ROTMGProgramLog.txt','w')
    f.write('')
    f.close()
logging.basicConfig(
    filename='ROTMGProgramLog.txt',
    level=logging.DEBUG, 
    format=' %(asctime)s - %(levelname)s - %(message)s')

logging.disable(level=logging.DEBUG) # this will disable logging and slightly increase the 
# speed of the program
logging.info('Start of program')

#SETTING UP FAILSAFES
pyautogui.PAUSE = .00 # wait 1.5 seconds after each function call.
#(user input or just waiting, but mostly just waiting)
pyautogui.FAILSAFE = True
#pyautogui.FailSafeException




#I had a Win 5 error when clicking, but it would still click, so this will bypass the error
def clickFix():
    try:
        pyautogui.click()
    except PermissionError:
        pass

# create Game Overlay in the CMD Console
def createGameOverlay():
    logging.info("Update GAME OVERLAY")
    logging.debug("clear the overlay")
    os.system('cls')
    print('Click on this Overlay and Press Ctrl-C to quit.')

    global gameStatus
    global whereStr
    global autoNexusCount
    
    statusStr = ' GameStatus: ' + gameStatus.rjust(7) + '\n'
    statusStr +='  RealmName: ' + whereStr.rjust(7) + '\n'
    statusStr +='AutoNexused: ' + str(autoNexusCount).rjust(7) + '\n'

    print(statusStr, end='\n')
    global updateOnNextRun
    updateOnNextRun = False
    logging.debug("finished printing the overlay")

def openUpROTMG():
    global xScreenScale
    global yScreenScale
    global steamIsClosed
    global gameStatus
    global updateOnNextRun
    logging.info("opening Up ROTMG")
    trayLoc = searchPNG("SteamTrayIcon",center=True)
    pyautogui.moveTo(trayLoc[0]*xScreenScale, trayLoc[1]*yScreenScale)
    pyautogui.click(button="right")
    time.sleep(2/3)
    trayLoc = pyautogui.locateCenterOnScreen("ROTMGDropdown.png") #region = (trayLoc[0] - 200, trayLoc[1]+30, 50,100) )
    logging.error("trayloc must not be None" + str(trayLoc))
    pyautogui.moveTo(trayLoc[0]*xScreenScale, trayLoc[1]*yScreenScale)
    pyautogui.click(button = "left")
    logging.debug("ROTMG is coming into focus")
    time.sleep(7.5)
    a = pyautogui.locateOnScreen("ROTMGTrayIconOpenAndFocused.png")
    if a == None:
        logging.debug("steam should be opening, this could take a while")
        time.sleep(60)
        a = pyautogui.locateOnScreen("ROTMGTrayIconOpen.png")
    if a == None:
        logging.error("Where is the rotmg Window?")
        pyautogui.screenshot("DebugScreenshot.png")
        raise exception("ROTMG is unable to open")
    if a != None:
        logging.debug("ROTMG is open")
        #pyautogui.moveTo(a[0]*xScreenScale,a[2]*yScreenScale)
        #pyautogui.click()
        #time.sleep(5)
        #logging.debug("Just clicked on the ROTMG Tray. The window should be focused (green)")
    titleLoc = searchPNG("ROTMGTitleGreen")
    if titleLoc == None:
        logging.error("where is the ROTMG TITLE?")
        pyautogui.screenshot("DebugScreenshot.png")
        raise exception("where is the ROTMG TITLE?")

    pyautogui.moveTo((titleLoc[0]+titleLoc[2])*xScreenScale,(titleLoc[1]+titleLoc[3])*yScreenScale)
    #pyautogui.click(titleLoc[0]*xScreenScale,titleLoc[1]*yScreenScale)
    #time.sleep(2)
    
    pyautogui.dragTo(50,60, duration = 0)

    steamIsClosed = False
    gameStatus = "Running"
    updateOnNextRun = True
    
#finds the corners of the ROTMG window to increase pixel searching efficiency
def whereROTMGWindow():
    logging.info("finding the ROTMG Window edges")
    time.sleep(.1)
    im = Image.open("greenTitleBar.png").convert(mode="RGB")
    px = im.load()

    mainWinPixel = (119,156,72)
    edgeWinPixel = (130,163,88)

    # print(px[0,1]) # yields (119,156,72) which is the main green
    # print(px[1,1]) # yields (119,156,72) which is the main green
    # print(px[1,0]) # yields (130,163,88) which is the lighter green

    screenshot = pyautogui.screenshot()
    pretitleLoc = pyautogui.locateOnScreen(im)
    if pretitleLoc == None:
        im = Image.open("greenTitleBar2.png")
        pretitleLoc = pyautogui.locateOnScreen(im)
        if pretitleLoc == None:
            return None

    leftmostPre = (pretitleLoc[0]-pretitleLoc[2]/2 ,pretitleLoc[1],pretitleLoc[2],pretitleLoc[3])
    print("leftmost of the searched image ", leftmostPre)
    # f = pyautogui.screenshot("debug.png", leftmostPre)
    #f.show()

    x,y = pyautogui.size()
    logging.debug("x, y = " + str( x) + ", " + str(y))

    xscale = x/1920 #only needed for mouseclicks
    yscale = y/1080

    #TODO iterate to the top pixel that matches
    topLeftLoc = list(leftmostPre[0:2])
    #print(topLeftLoc)
    # print(im.load()[(0,1)])
    # print(screenshot.load()[(topLeftLoc[0],topLeftLoc[1])])

    print ("iterating to the top of the window")
    while mainWinPixel == screenshot.load()[topLeftLoc[0],topLeftLoc[1]]:
        topLeftLoc[1] += -1
        if topLeftLoc[1] == 0:
            break
    if screenshot.load()[topLeftLoc[0],topLeftLoc[1]] != edgeWinPixel:
        topLeftLoc[1] += 1

    #TODO iterate to the left pixel that matches
    topEdgePixel = screenshot.load()[topLeftLoc[0],topLeftLoc[1]]
    print ("iterating to the leftedge of the window")
    while topEdgePixel == screenshot.load()[topLeftLoc[0],topLeftLoc[1]] and topLeftLoc[0] >0:
        topLeftLoc[0] += -1
        if topLeftLoc[0] == 0:
            break
    if (screenshot.load()[topLeftLoc[0],topLeftLoc[1]] != edgeWinPixel and
        screenshot.load()[topLeftLoc[0],topLeftLoc[1]] != mainWinPixel
        ) :
        topLeftLoc[0] += 1
    logging.debug(str(topLeftLoc))
    #TODO iterate to the right pixel that matches
    bottomRightLoc = list((topLeftLoc[0]+1,topLeftLoc[1]))
    leftEdgePixel = screenshot.load()[bottomRightLoc[0],bottomRightLoc[1]]
    print ("iterating to the rightedge of the window")
    while leftEdgePixel == screenshot.load()[bottomRightLoc[0],bottomRightLoc[1]] and bottomRightLoc[1] < y :
        bottomRightLoc[0] += 1
        if bottomRightLoc[0] == x:
            break
    if (screenshot.load()[bottomRightLoc[0],bottomRightLoc[1]] != edgeWinPixel and
        screenshot.load()[bottomRightLoc[0],bottomRightLoc[1]] != mainWinPixel
        ) :
        bottomRightLoc[0] += -1
    logging.debug(str(bottomRightLoc))
    #TODO iterate to the bottom pixel that matches
    bottomEdgePixel = screenshot.load()[bottomRightLoc[0],bottomRightLoc[1]]
    print ("iterating to the bottomedge of the window")
    while bottomEdgePixel == screenshot.load()[bottomRightLoc[0],bottomRightLoc[1]] and bottomRightLoc[0] < x :
        bottomRightLoc[1] += 1
        if bottomRightLoc[1] == y:
            break
    if (screenshot.load()[bottomRightLoc[0],bottomRightLoc[1]] != edgeWinPixel and
        screenshot.load()[bottomRightLoc[0],bottomRightLoc[1]] != mainWinPixel
        ) :
        bottomRightLoc[1] += -1
    logging.debug(str(bottomRightLoc))
    w,h = [a_i - b_i for a_i, b_i in zip(bottomRightLoc, topLeftLoc)] 
    return (topLeftLoc[0],topLeftLoc[1],w,h)

def searchPNG(fileRootStr,region=None,center=False):
    if center == False:
        if region == None:
            for filename in os.listdir():
                if len(filename) < len(fileRootStr) + 4: continue
                if filename[-4:] != ".png": continue
                if filename[:len(fileRootStr)] == fileRootStr:
                    Loc = pyautogui.locateOnScreen(filename)
                    if Loc != None:
                        logging.info(filename + " matches PX on screen")
                        return Loc
        else: #there is a specified region
            for filename in os.listdir():
                if len(filename) < len(fileRootStr) + 4: continue
                if filename[-4:] != ".png": continue
                if filename[:len(fileRootStr)] == fileRootStr:
                    Loc = pyautogui.locateOnScreen(filename, region=region)
                    if Loc != None:
                        logging.info(filename + " matches PX on screen")
                        return Loc
    else:
        if region == None:
            for filename in os.listdir():
                if len(filename) < len(fileRootStr) + 4: continue
                if filename[-4:] != ".png": continue
                if filename[:len(fileRootStr)] == fileRootStr:
                    Loc = pyautogui.locateCenterOnScreen(filename)
                    if Loc != None:
                        logging.info(filename + " matches PX on screen")
                        return Loc
        else: #there is a specified region
            for filename in os.listdir():
                if len(filename) < len(fileRootStr) + 4: continue
                if filename[-4:] != ".png": continue
                if filename[:len(fileRootStr)] == fileRootStr:
                    Loc = pyautogui.locateCenterOnScreen(filename, region=region)
                    if Loc != None:
                        logging.info(filename + " matches PX on screen")
                        return Loc
    #return the location of the PNG


def whereIam(region=(0,0,1920,1080)):
    logging.info( "Updating Where Vars")
    a = time.time()
    global whereLoc
    global whereStr
    global whereIMG
    logging.debug("beginning searches")
    whereLoc = None
    if whereLoc == None:
        whereLoc = searchPNG("InARealm", region = region)
    if whereLoc != None:
        whereStr = "Realm"
        whereIMG = pyautogui.screenshot(region = whereLoc)
        logging.info("it took " + str(time.time()-a) + " seconds to find.")
        return
    if whereLoc == None:
        whereLoc = searchPNG("InNexus", region = region)
    if whereLoc != None:
        whereStr = "Nexus"
        whereIMG = pyautogui.screenshot(region = whereLoc)
        logging.info("it took " + str(time.time()-a) + " seconds to find.")
        return
    if whereLoc == None:
        whereStr = "Unknown"
        logging.info("it took " + str(time.time()-a) + " seconds to finish searches.")
        
def autoNexuser():
    global whereLoc
    global whereIMG #.load()
    global whereStr
    global winLoc

    global badHPPixelRGB
    global badHPPixelRGB2
    
    global autoNexusCount

    logging.debug(
        "this is if the whereloc equals the whereIMG" +
        str(pyautogui.locateOnScreen(whereIMG)) +
        str(whereLoc) )
    # logging.debug("is whereIMG the same size as WhereLoc?" + str(whereIMG.size != whereLoc))
    # if whereIMG.size != whereLoc: whereIam()

    # logging.debug(     "If this is 0,0,0 then the two images are the same"+ '\n'+
    #     str(ImageChops.difference(whereIMG, pyautogui.screenshot(region = whereLoc)))+ '\n'+
    #     str(sum(ImageStat.Stat(ImageChops.difference(whereIMG, pyautogui.screenshot(region = whereLoc))).var))
    #     )
    
    logging.info("running autonexus ops")
    
    d = time.time()
    e = 0
    logging.debug("alternative image comparison " + 
        str(whereIMG == pyautogui.screenshot(region = whereLoc))
        )    
    
    #the autonexuser needs to hve HPBar be an address
    if HPBar[0] == 0:
        a = pyautogui.locateOnScreen("BeginningOfHPBar.png", region=winLoc)
        if a != None:       
            x,y,w,h = a
            HPBar[0] = x
            HPBar[1] = y
        else: 
            logging.critical("WHERE IS THE HP BAR? I made a screenshot")
            print("WHERE IS THE HP BAR? I made a screenshot")
            pyautogui.screenshot("DebugScreenshot.png")
    HPLoc = (HPBar[0]+ HPBar[2]*nexusAtHPPercent,HPBar[1]+.5*HPBar[3],1,1)


    f = whereIMG.convert(mode="1") #to make checking this more efficient will be greyscale and cropped
    while f == pyautogui.screenshot(region = whereLoc).convert(mode="1"):
        #Reporting what is being done
        e += 1
        if (time.time() - d) >= 60 :
            logging.info("Checked the HP " + str( e) + " times last minute.")
            print("Checked the HP " + str( e) + " times last minute.", end = '\r')
            e = 0
            d = time.time()
        
        #this will send you to the nexus if you have selected the
        #ROTMG window
        #print("the value of b is" + str(b))
        impx = pyautogui.screenshot(region = HPLoc).getpixel((0,0))
        logging.debug("current value of hppixel is" + str(impx))
        
        if ((impx == badHPPixelRGB) or (impx == badHPPixelRGB2)): # then your health is under 20 percent
            logging.debug("bad HP pixel is" + str(impx))
            pyautogui.typewrite(["r", "enter" , "r"])
            time.sleep(1)
            autoNexusCount += 1
            logging.debug("Just nexused for the " + str(autoNexusCount) + " time(s)")
            return
    whereStr = "JustTeleported"

# TODO create a web scraper that determines from the wiki what projectiles
# damages are for whatever dungeon

# TODO create a midlands fame train-esque guy
# who is able to identify and call candylands

# TODO automate the fametrain

#### BEGINNING OF MASTER FILE
try:
    #setting up global variables
    x,y = pyautogui.size()
    updateOnNextRun = True
    steamIsClosed = True
    xScreenScale = x/1920
    yScreenScale = y/1080
    nexusAtHPPercent = .20
    goodHPPixelRGB = (197,45,45)
    goodHPPixelRGB2 = (224, 52, 52)
    goodHPPixelRGB3 = (213, 54, 54)
    badHPPixelRGB = (73,73,73)
    badHPPixelRGB2 = (84,84,84)
    HPBar = [0,0,219,18] #begin pixel x,y and x width and y height
    #im = pyautogui.screenshot()
    gameStatus = "Closed"
    autoNexusCount = 0
    winLoc = None
    whereStr = "Unknown"
    whereLoc = None
    whereIMG = None
    # This is the constant series of instructions
    openUpROTMG()
    winLoc = whereROTMGWindow()
    winIMG = pyautogui.screenshot(region= (winLoc[0],winLoc[1],30,30)).convert(mode="1")
    
    while True:
        
        # TODO if the ROTMG WINDOW has moved, update its edges
        if winIMG != pyautogui.screenshot(region= (winLoc[0],winLoc[1],30,30)).convert(mode="1"):
            winLoc = whereROTMGWindow()
            if winLoc == None:
                logging.info("The ROTMG window has closed")
                print("The ROTMG window has closed")
                break
            else:
                winIMG = pyautogui.screenshot(region= (winLoc[0],winLoc[1],30,30)).convert(mode="1")
                HPBar[0:2] = 0,0
                updateOnNextRun = True
        # TODO if the ROTMG WINDOW is closed, break from this while loop

        #set up the CMD Overlay if it needs to be updated
        if updateOnNextRun:
            createGameOverlay()

      
        # EnterARealm.png refers to the picture you pick when you click enter. I hope 
        #to map this to a key like T or Y
        
        a = whereStr
        whereIam(winLoc) #update vars
        if whereStr != a:
            updateOnNextRun = True
            continue

        if whereStr == "Realm":
            autoNexuser()
            updateOnNextRun = True

        #TODO if I am in the nexus, I want to constantly check for "FULL" and the mouse position
        # then autoclick like crazy until the whereIMG picture changes.
        if whereStr == "Nexus":
            continue
            
except KeyboardInterrupt:
    print('\nDone.')
    logging.debug('End of program')
#except FailSafeException:
#    print('\nDone.')
#### END OF MASTER FILE
