from mainInput import main as INPUT
from mainOutput import main as OUTPUT

def main():
    while True:
        whatHeWants = input('If you want to view what have you bought today, type "1", if you want to ann new receipt, type "2" If you want to stop write done: ')
        if whatHeWants == '1':
            OUTPUT()
        elif whatHeWants == '2':
            INPUT()
        elif whatHeWants == 'done':
            return
    
if __name__ == "__main__":
    main()
    