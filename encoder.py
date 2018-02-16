''' Digital communication assignment    '''
''' Encodes texts into their Huffman encoding        '''
''' Python 3.5.2        '''

''' importing the pkgs & libs   '''
import decimal
import gzip
import numpy as np
import operator
import os
import sys


''' reading the file    '''
fileAddr = sys.argv[1]          # get file address via argument - Texts/CEM.txt

with open(fileAddr, 'r') as f:
    text = f.read()


''' setup dictionary of individual characters and their respective probabilities   '''
charProb = {}

# add occurences of each character to dictionary
for char in text:
    if char not in charProb:
        charProb[char] = 1
    else:
        charProb[char] += 1

# normalize frequencies into probabilities
for char in charProb:
    charProb[char] /= len(text)


''' Huffman class to determine encodings and encode chars '''
class Huffman:

    # initialise dictionary to contain encodings for each char
    def __init__(self):
        self.charEncodings = {}         # dict to store the Huffman encodings for each char after being determined


    # return an encoding for a given char
    def encodeChar(self, char):
        return self.charEncodings[char]


    # determine the encodings for each char based in the probabilities
    def fit(self, workingCharProb):

        # sorting the dictionary by character probability
        workingCharProb = sorted(workingCharProb.items(), key=operator.itemgetter(1))

        # function to get the number of decimal places of a float
        decimalPlacesNo = lambda X: abs(decimal.Decimal(str(X)).as_tuple().exponent)

        # until there are only two elements left in the working dictionary (most probable char and the combination of the others)
        while len(workingCharProb) >= 2:
            #print (workingCharProb)

            # extract two least probable letters from dict
            lastChar, secondLastChar = workingCharProb[0][0], workingCharProb[1][0]

            # extract probabilities of two least probable chars
            lastProb, secondLastProb = workingCharProb[0][1], workingCharProb[1][1]

            # if is a single char, set preliminary encoding to 1
            if (len(lastChar) == 1):
                self.charEncodings[lastChar] = '1'
            else:
                # if multiple chars, add the encoding 1 to the front of the current encoding for each of those chars
                for char in lastChar:
                    self.charEncodings[char] = '1' + self.charEncodings[char]

            if (len(secondLastChar) == 1):
                self.charEncodings[secondLastChar] = '0'
            else:
                for char in secondLastChar:
                    self.charEncodings[char] = '0' + self.charEncodings[char]


            # remove least two probable chars
            workingCharProb = workingCharProb[2:]

            # combine the strings of the two least probable chars
            combinedChar = lastChar + secondLastChar

            # combine the probabilities of the two least probable chars
            combinedProp = round(lastProb + secondLastProb, np.max([decimalPlacesNo(lastProb), decimalPlacesNo(secondLastProb)]))

            # append the combinations to the new list of probabilities
            workingCharProb.append((combinedChar, combinedProp))

            # sort the list by probabilities before starting manipulation again
            workingCharProb = sorted(workingCharProb, key=operator.itemgetter(1))

            #print (self.charEncodings)


''' Determine the Huffman encodings for each char of the message    '''
h = Huffman()
h.fit(charProb)
encodedText = str()

# encode the text with huffman encodings
for char in text:
    encodedText += h.encodeChar(char)


''' Writing output to file '''
# store dictionary along with encoded text in output
outputText = (str(h.charEncodings) + encodedText).encode('utf-8')
outFileName = fileAddr.replace('txt', 'hc')

with gzip.open(outFileName, 'wb') as f:
    f.write(outputText)

#print (text)
#print (outputText)


''' File size ratio   '''
print ('Compression ratio:', os.path.getsize(fileAddr) / os.path.getsize(outFileName))
