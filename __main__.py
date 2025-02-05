from mainInput import main as INPUT
from mainOutput import main as OUTPUT

def main():
    while True:
        print('WELCOME TO THE RECEIPT APP MAIN MENU')
        print('If you want to view what have you bought today, type "1", ')
        print('if you want to ann new receipt, type "2" ')
        print('If you want to stop write "done": ', end='')
        whatHeWants = input()
        if whatHeWants == '1':
            OUTPUT()
        elif whatHeWants == '2':
            INPUT()
        elif whatHeWants == 'done':
            return
    
if __name__ == "__main__":
    main()
    