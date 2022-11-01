x = "Yvzs! I xzm'g yvorvev Lzmxv olhg srh qly zg gsv xlolmb!!"
    # x is a string, like "vmxibkgrlm"
    # output should be "encryption"
    
    # step 0, split into words
    # step 1, split words into char arrays
    # rotate function on all lower case letters (not punctuation)
    ## check if unicode >= 141 (a) or <=172 (z)
    ### if yes, then swap
    ### if no, do nothing to this char
    ## merge letters back into words
    # merge words back into string
    # return
    
    # swap function will be if unicode <= 155
    ## offset = 'm' - unicode
    ## result = 'z' - offset
    # else
    ## offset = unicode - 'n'
    ## result = 'm' - offset
    
words = x.split(" ")
word_swapped = ""
string_swapped = ""

for word in words:
    for letter in word:
        if ord(letter) >= ord('a') and ord(letter) <= ord('z'):
            if ord(letter) <= ord('m'):
                offset = ord('m') - ord(letter)
                result = ord('n') + offset
            else:
                offset = ord(letter) - ord('n')
                result = ord('m') - offset
            word_swapped = word_swapped + chr(result)
            # print("lower case!")
        else:
            # print("not lower case")
            word_swapped = word_swapped + letter
    word_swapped = word_swapped + ' '

print( word_swapped )

        