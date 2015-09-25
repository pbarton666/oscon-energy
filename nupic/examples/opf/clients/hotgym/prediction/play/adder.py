'''
adder.py
adds two numbers only if both are integers
'''

def adder_errors(x,y):
    """
    Adds two integers
    """
    if isinstance(x, int) and isinstance(y,int):
        return x+y 
    else:
        raise TypeError

#adder_errors(2, "a")