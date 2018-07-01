''' Digital communication assignment    '''
''' Decodes texts into from Huffman encoding into plain format        '''
''' Python 3.5.2        '''

''' importing the pkgs & libs   '''
import ast
import gzip
import numpy as np
import sys


''' reading the file    '''
fileAddr = sys.argv[1]          # get file address via argument - Texts/CEM.hc
fileExt = fileAddr.split('.')[-1]
if not(fileExt == 'hc'):
    raise ValueError('File extension not .hc!')

with gzip.open(fileAddr, 'rb') as f:
    encodedText = f.read().decode('utf-8')


''' extract dictionary of characters from input   '''
# find index of outer bracket of dictionary within the compressed text
endDictIndex = np.max([encodedText.find('}0'), encodedText.find('}1')]) + 1

# extracting dictionary from text
dictionary = ast.literal_eval(encodedText[:endDictIndex])

# remove dictionary from input, now only the Huffman encoded text
encodedText = encodedText[endDictIndex:]


''' decoding the Huffman text using the dictionary   '''
decodedText = str()
charForDecoding = str()
currentCharIndex = 0        # the index of the encoded string at which we are trying to decode

# iterate through the encoded text
while currentCharIndex < len(encodedText):

    # check a subset of encoded text against the encoding for each char in the dictionary
    for key, value in dictionary.items():

        encodingLength = len(value)

        # get subset of encoded text which is the same length as an encoding in the dictionary
        # eg. if some encoding is 0011 for some character, look at the next four bits in the encoded text to see if it matches
        # do this for each entry in the dictionary
        if encodedText[currentCharIndex: currentCharIndex + encodingLength] == value:

            # add decoded letter to decoded string and increment index
            decodedText += key
            currentCharIndex += encodingLength

#print (decodedText)


''' Writing decoded output to file '''
outFileName = fileAddr.replace('hc', 'out')

with open(outFileName, 'w') as f:
    f.write(decodedText)
