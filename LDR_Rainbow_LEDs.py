'''
Python program to turn on strips of LEDs sequencially, in rainbow colour strips when the lux (light) level goes below 25.
'''
#Import necessary code
from motephat import * #Light strip code
from threading import Thread #Threading code - to run multiple code at the same time
from envirophat import light #Light-sensing code
from time import sleep #Pausing code
from colorsys import hsv_to_rgb #Colour conversion code - from HSV (a format used to create rainbows) to RGB (the format used by the lights - Red Green Blue)

lights_running = False #Set the lights to not run, by using a variable - data storage box - called 'lights_running'
                
def read_lux(): #Set up light-reading function
    lux = light.light() #Read the lux level
    return lux #Return the lux level

def monitor_lux(): #Set up monitoring function
    global lights_running #Use the 'lights_running' variable in the function
    
    while True: #Loop infinitely
        lux = read_lux() #Read the lux - light - level using pre-defined function
            
        while not lux < 25: #While the light level is not greater than 25 lux - this loop waits until the lux level to be dark:
            lux = read_lux() #Read the lux level again
            print(lux) #Output the lux level
            sleep(0.1) #Pause for a tenth of a second

        #When out of that loop, lux is greater than 25 -  turn on lights
        lights_running = True #Tell lights to turn off
        
        while not lux >= 25: #While the light level isn't greater than or equal to 25 - while lights should be on (this loop waits until the lux level is light again):
            lux = read_lux() #Read the light again
            print(lux) #Output the lux level
            sleep(0.1) #Pause for a tenth of a second

        #When out of the loop, lux is less than 25 - turn off lights
        lights_running = False #Tell lights to turn off

light_monitor = Thread(target=monitor_lux) #Set up pre-defined light monitoring program as a 'Thread' - runs in the background
light_monitor.start() #Run the light monitoring thread

print('Monitoring Light Level...') #Output notice 'Monitoring Light Level...'

clear() #Clear the lights
show() #Show the current lights setting (show the blank LEDs)

while True: #Loop infinitely
    while not lights_running: #While the lights aren't set to run:
        sleep(0.1) #Pause for a tenth of a second (wait for the lights to run)
    
    while True: #Loop infinitely
        for i in range(0, 100, 7): #Loop for a number of times from 0 to 100 with a step of 7, with variable 'i' holding the loop number. This loop is to cycle through the HSV colours.
            for x in range(16): #Loop 16 times, with 'x' holding the loop number - this is a nested loop, and this loop will repeat inside the other loop. This loop is to go through the individual LED one by one.

                if not lights_running: #If the variable 'lights_running' isn't true (the lights aren't meant to be running):
                    clear() #Clear the lights
                    show() #Show the current lights setting (show the blank LEDs)
                    
                    while not lights_running: #While the lights aren't running (this loop waits until the lights should be on again):
                        sleep(0.1) #Pause for a tenth of a second
                        
                    break #When the lights need to go on, break out of the loop (so we can do it all again!)
                    
                else: #If the lights are meant to be running (variable 'lights_running' is false), turn the lights on:
                    rgb = hsv_to_rgb(float(i) / 100.0, 1.0, 1.0) #Get the RGB colour value from the HSV colour value of 'i' - HSV is used becuase the numbers between 1 and 100 go in a rainbow, though this value needs to be a decimal
                    set_pixel(1, x, round(rgb[0] * 255), round(rgb[1] * 255), round(rgb[2] * 255)) #Set the LED in the 'x' position of the 1st strip to the correct RGB value (although the values have to be multiplied by 255)
                    set_pixel(2, x, round(rgb[0] * 255), round(rgb[1] * 255), round(rgb[2] * 255)) #Set the LED in the 'x' position of the 2nd strip to the correct RGB value (although the values have to be multiplied by 255)

                    show() #Show what the lights have been set to
                    sleep(0.1) #Pause for a tenth of a second
