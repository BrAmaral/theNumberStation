#Imports
import os           # For OS command execution

#Functions
def printMenu():
    print("""

┏━━━━┓┏┓━━━━━━━━━━┏━┓━┏┓━━━━━━━━┏┓━━━━━━━━━━━━━┏━━━┓━┏┓━━━━━━━┏┓━━━━━━━━━━━
┃┏┓┏┓┃┃┃━━━━━━━━━━┃┃┗┓┃┃━━━━━━━━┃┃━━━━━━━━━━━━━┃┏━┓┃┏┛┗┓━━━━━┏┛┗┓━━━━━━━━━━
┗┛┃┃┗┛┃┗━┓┏━━┓━━━━┃┏┓┗┛┃┏┓┏┓┏┓┏┓┃┗━┓┏━━┓┏━┓━━━━┃┗━━┓┗┓┏┛┏━━┓━┗┓┏┛┏┓┏━━┓┏━┓━
━━┃┃━━┃┏┓┃┃┏┓┃━━━━┃┃┗┓┃┃┃┃┃┃┃┗┛┃┃┏┓┃┃┏┓┃┃┏┛━━━━┗━━┓┃━┃┃━┗━┓┃━━┃┃━┣┫┃┏┓┃┃┏┓┓
━┏┛┗┓━┃┃┃┃┃┃━┫━━━━┃┃━┃┃┃┃┗┛┃┃┃┃┃┃┗┛┃┃┃━┫┃┃━━━━━┃┗━┛┃━┃┗┓┃┗┛┗┓━┃┗┓┃┃┃┗┛┃┃┃┃┃
━┗━━┛━┗┛┗┛┗━━┛━━━━┗┛━┗━┛┗━━┛┗┻┻┛┗━━┛┗━━┛┗┛━━━━━┗━━━┛━┗━┛┗━━━┛━┗━┛┗┛┗━━┛┗┛┗┛
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        1 - Encode Message
        2 - Decode Message
        3 - Exit

        """)

def printEncodeInstructions():
    print("""
.--------------.
| Instructions |
'--------------'
1) The one-time-pad must be the same length as the message.
    
2) The codephrase can be whatever you want. It exists to tell the agent where to find the Pad (<CODEPHRASE> <NUMBER> e.g. ASCENSION 7)
    
3) The one-time-pad is case-sensitive

4) The pad uses ASCII chars only! Check the ASCII table.

5) The pad must be somewhat random. Using books or magazines segments is a viable option.


""")

def printDecodeInstructions():
    print("""
.--------------.
| Instructions |
'--------------'
1) Paste only the numbers equivalent to the message, discard the CODEPHRASE (and any number related to it, if any)

""")

def clearScreen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def waitUserInput():
    input()

def menu():
    inp = True
    clearScreen()
    
    while(inp):    
        clearScreen()
        printMenu()
        
        inp = input("Choose an option: ")
        if inp == "1":
            encodeMessage()

        elif inp == "2":
            decodeMessage()

        elif inp == "3":
            clearScreen()
            print(" ▌║█║▌│║▌│║▌║▌█║End of Transmission ▌│║▌║▌│║║▌█║▌║█\n\n")
            inp = None
        
        else:
            clearScreen()
            print("The input is not valid, please try again.")
            print("Press any key...")
            waitUserInput()
            clearScreen()

def encodeMessage():
    clearScreen()
    printEncodeInstructions()
    
    message = list(str(input("\nEnter your message: ")).encode('ascii'))
    print("The message length is: " + str(len(message)))
    
    pad = list(str(input("\nEnter your pad: ")).encode('ascii'))
    
    if len(message) == len(pad):
        codephrase = str(input("Enter the Codephrase: "))
        print(codephrase, end=" ")
        calculateNumbers(message, pad)
    else:
        clearScreen()
        print("The pad length is: " + str(len(pad)))
        print("\nThe message and the pad does not have the same length. Please try again...")
        print("Press any key...")
        waitUserInput()
        encodeMessage()

def decodeMessage():
    clearScreen()
    printDecodeInstructions()

    codedMessage = input("\nEnter the numbers: ").split()
    print("The message length is: " + str(len(codedMessage)))
    codedMessage = [int(i) for i in codedMessage]
    pad = list(str(input("\nEnter your pad: ")).encode('ascii'))

    if len(codedMessage) == len(pad):
        calculateNumbersReverse(codedMessage, pad)
    else:
        print("The pad length is: " + str(len(pad)))
        print("\nThe numbers and the pad does not have the same length. Please try again...")
        print("Press any key...")
        waitUserInput()
        decodeMessage()

def calculateNumbers(message, pad):
    index = 0
    for loop in message:
        #Bug --- The print is showing in the menu for some reason... it will become a feature
        print((loop - pad[index])%127, end=' ')
        index = index + 1

def calculateNumbersReverse(codedMessage, pad):
    index = 0
    for loop in codedMessage:
        print(chr((loop + pad[index])%127), end = '')
        index = index + 1

#Main Function
def main():
    menu()

#Default condition
if __name__ == '__main__':
    main()