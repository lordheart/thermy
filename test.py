
def chunks(s, n):
    #yield 'n' -characters chunks from 's'.
    for start in range(0, len(s), n):
        yield s[start:start+n]
    
def printUpsideDown(longString, charPerLine=32):
    split = []
    for chunk in chunks(longString, charPerLine):
        split.insert(0,chunk)
    for s in split:
        print s + "\n"


printUpsideDown("123456789012345678901234567890123456789012345678901234567891234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678900")
