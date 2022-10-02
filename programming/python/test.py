s = ["A"," ","m","a","n",","," ","a"," ","p","l","a","n",","," ","a"," ","c","a","n","a","l",":"," ","P","a","n","a","m","a"]

length = len(s)-1
    
for i in range(int(length/2)):
    ## store the var we're over writing, then swap left and right
    tmp = s[i]
    s[i] = s[length-i]
    s[length-i] = tmp


print("output = {0}".format(s))