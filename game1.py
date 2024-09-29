import time
import sys

def typewriter(text, delay=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()  
        time.sleep(delay)  
    print()  

def Text_TIMECHANGE(text, delay= 0.1):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()  
        time.sleep(delay)  
    print()  


typewriter("A Grape Guy Production... ")
Text_TIMECHANGE("  ")
typewriter("After a long Journey, Learning Python, Encryption Stuff and Whatever,")
Text_TIMECHANGE("  ")
typewriter("Welcome to... ")
Text_TIMECHANGE("    ")
print("THE GRAPEST GAME EVER")
print(" ")
print(" ")
print(" ")
print(" ")

def name():
    global name
    name = str(input("What Is Your Travelers Name? "))
name()

def stats(): 
    global Strength 
    global Defense
    global Speed
    global Magic
    Strength = int(input("Please input your Strength "))
    Strength = int(input("Please input your Defense "))
    Strength = int(input("Please input your Speed "))
    Strength = int(input("Please input your magic"))
stats()


