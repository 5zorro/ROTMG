#! python3
#! CMDSandbox.py
import pyautogui, time, os

os.system('cls') #this clears the Command line
positionStr = "pqrstuvwxyz"
print("abcdefg" + '\n' + "hijklmno" + '\n' + "pqrstuvwxyz",end='\r',flush=True)
print('\b' * len(positionStr), end='', flush=True) #this blanks out the last line


