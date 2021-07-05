import requests
word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
response = requests.get(word_site)
words = response.content.splitlines()

def encrypt(keyMap, text, key):
    conStr = ''
    if keyMap == 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        text = text.upper()
    for character in text:
        location = keyMap.find(character)
        if location == -1:
            conStr += character
        else:
            conStr += keyMap[(location + key) % (len(keyMap))]
    return '\n' + conStr + '\n'

while True:
    decrypt = False
    smartBruteForce = False
    bruteForceFilter = False
    while True:
        keyMap = input('What keymap do you want to use? The options are:\nROT13\nROT47\nCustom\n').lower()
        if keyMap not in ['rot13', 'rot47', 'custom']:
            continue
        if keyMap == 'rot13':
            keyMap = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        elif keyMap == 'rot47':
            keyMap = '!"#$%& \'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
        elif keyMap == 'custom':
            while True:
                keyMap = input('Enter your custom keymap:\n')
                unique = True
                for char in keyMap:
                    if keyMap.count(char) != 1:
                        unique = False
                if unique == True:
                    break
                else:
                    print('Your keymap had multiple instances of the same character.')
                    #TODO: multi-instance decryption and encryption         
        break 
            
    while True:
        bruteForce = input('Do you want to encrypt or decrypt?\n').lower()
        if bruteForce not in ['encrypt', 'decrypt']:
            continue
        elif bruteForce == 'decrypt':
            decrypt = True
            bruteForce = input('Do you want to use brute force decryption?\n').lower()
            if bruteForce == 'yes':
                if input('Do you have a string that you know is in the decoded message?\n').lower() == 'yes':
                    bruteForceFilter = True
                    filterString = input('Enter the string here: ').upper()
                elif input('Do you want to enable the output analyzer? This is an experimental feature for decrypting messages.\n').lower() == 'yes':
                    smartBruteForce = True
                    print('ANALYZER ACTIVATED')
            break
        else:
            break
    text = input('Please enter your text here: ')
    if bruteForce == 'yes':
        for possibility in range(len(keyMap) - 1):
            result = encrypt(keyMap, text, possibility)
            if smartBruteForce == True:
                for word in words:
                    word = word.decode('utf-8').upper()
                    if word in result and len(word) > 3:
                        print(result)
                        break
            elif bruteForceFilter == True:
                if filterString in result:
                    print(result)
            else:
                print(result)
    else:
        while True:
            try:
                key = int(input('Please enter your encryption/decryption key: ')) % (len(keyMap) - 1)
                if key < 0:
                    continue
                else:
                    break
            except ValueError:
                continue
        if decrypt == True:
            key = -(key)
        print(encrypt(keyMap, text, key))
