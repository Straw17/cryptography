import re
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
letterFreq = [0.08167,0.01492,0.02782,0.04253,0.12702,0.02228,0.02015,0.06094,0.06966,0.00153,0.00772,0.04025,0.02406,0.06749,0.07507,0.01929,0.00095,0.05987,0.06327,0.09056,0.02758,0.00978,0.02360,0.00150,0.01974,0.00074];
regex = re.compile('[^A-Z]')

def findFactors(n):
  factorValues = []
  for i in range(1, n + 1):
    if n % i == 0:
      factorValues.append(i)
  return factorValues

def decrypt(text, key):
    conStr = ''
    for character in text:
        location = alphabet.find(character)
        conStr += alphabet[(location - key) % (len(alphabet))]
    return conStr

def decryptVigenere(text, key):
    conStr = ''
    for character in range(len(text)):
        location = alphabet.find(text[character])
        conStr += alphabet[(location - alphabet.find(key[character%(len(key))])) % (len(alphabet))]
    return conStr

def getIC(text):
    num = 0.0
    den = 0.0
    for letter in alphabet:
        freq = len([i for i, char in enumerate(text) if char == letter])
        num += freq * (freq - 1)
        den += freq
    if den <= 1.0:
        return 0.0
    else:
        return num / (den * (den - 1))

def getPeriod(text):
    periods = min([len(text)+1, 500])
    periodICChance = [0] * periods
    for period in range(1, periods):
        totalIC = 0;
        for sequence in range(period):
            toPass = ""
            for character in range(sequence, len(text), period):
                toPass += text[character]
            totalIC += getIC(toPass)
                
        if (totalIC/period) > 0.053:
            for factor in findFactors(period):
                if periodICChance[factor] != 0 or factor == period:
                    periodICChance[factor] += 1;
        print(str(period) + ": " + str(totalIC/(period)))
    return periodICChance.index(max(periodICChance))

def getChiSq(text):
    chiSqVal = 0
    for letter in range(26):
        #print(str(alphabet[letter]) + ': ' + str(letterFreq[letter] * len(text)))
        freq = len([i for i, char in enumerate(text) if char == alphabet[letter]])
        chiSqVal += ((freq - (letterFreq[letter] * len(text)))**2)/(letterFreq[letter] * len(text))
    return chiSqVal

def chiSqAnalysis(text, period):
    sequenceString = ""
    for sequence in range(period):
        chiVals = [0] * 26
        toPass = ""
        for character in range(sequence, len(text), period):
            toPass += text[character]
        for key in range(26):
            decryptedToPass = decrypt(toPass, key)
            chiVals[key] = getChiSq(decryptedToPass)
        sequenceString += alphabet[chiVals.index(min(chiVals))]
    return sequenceString

text = input('Enter text to crack: ').upper()
text = regex.sub('', text)
print("Chi Squared: " + str(getChiSq(text)))
print(getPeriod(text))
print(chiSqAnalysis(text, int(input("Enter period: "))))
print(decryptVigenere(text, input("Enter key: ")))
