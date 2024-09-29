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

