import pyautogui
import time 

"""
pyautogui.rightClick(100, 200)
time.sleep(5)
pyautogui.doubleClick(150, 250)

#pyautogui.dragTo(100, 500, duration=1.5)
time.sleep(1)
pyautogui.scroll(-500)  
"""

#time.sleep(5)
#pyautogui.click(773, 754)
#pyautogui.typewrite('Hello, unais', interval=0.2)
#pyautogui.write("python3 practice-py-autogui.py")
#pyautogui.press('enter')
#pyautogui.hotkey('command', 'tab','tab')

print(pyautogui.size())  # Returns the size of the primary monitor.

ss = pyautogui.screenshot()  # Takes a screenshot and saves it to a file.
ss.save('screenshot.png')