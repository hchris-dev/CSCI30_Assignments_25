import sys
import os
#from scrambled_flag_project. import main, functions, classes

print(sys.path)
sys.path.insert(0, "B:\Fall 2025 Courses\Python Programming\Midterm Project In VS\src")

for place in sys.path:
    print(place)
    
import scrambled_flag_project.main
