from math import gcd

print('''

╭━━╮╱╱╱╭╮╱╱╱╱╱╭━━━┳━━━┳━━━╮
┃╭╮┃╱╱╱┃┃╱╱╱╱╱┃╭━╮┃╭━╮┃╭━╮┃
┃╰╯╰┳━━┫╰━┳╮╱╭┫╰━╯┃╰━━┫┃╱┃┃
┃╭━╮┃╭╮┃╭╮┃┃╱┃┃╭╮╭┻━━╮┃╰━╯┃
┃╰━╯┃╭╮┃╰╯┃╰━╯┃┃┃╰┫╰━╯┃╭━╮┃
╰━━━┻╯╰┻━━┻━╮╭┻╯╰━┻━━━┻╯╱╰╯
╱╱╱╱╱╱╱╱╱╱╭━╯┃
╱╱╱╱╱╱╱╱╱╱╰━━╯
''')

def truncate(num):
    return int((num * 1000000)/1000000)

def primeFactors(primeNumber):
    i = 2
    factors = []
    while i * i <= primeNumber:
        if primeNumber % i:
            i += 1
        else:
            primeNumber //= i
            factors.append(i)
    if primeNumber > 1:
        factors.append(primeNumber)
    return factors

def removeDuplicates(primeFactorList):
    finalList = []
    for i in primeFactorList:
        if i not in finalList:
            finalList.append(i)
    return finalList

def findWholeNumberd(e, phi):
    for i in range(e):
        d = (1 + (i*phi))/e
        if(truncate(d) == d):
            return d


#First iteration, whether the code can find p and q from n e c

n = int(input("Enter given value of n: "))
e = int(input("Enter given value of e: "))

primeFactorList = primeFactors(n)
primeFactorList = removeDuplicates(primeFactorList)

print(primeFactorList)

if len(primeFactorList) != 2:
    print("Given value for n has", len(primeFactorList) , "prime factors and hence cannot be used for RSA Encryption or Decryption.")
    print("Exiting...")
    exit(1)
else:
    primeFactorList.sort()
    p = primeFactorList[0]
    q = primeFactorList[1]

phi = (p-1) * (q-1)

if(gcd(phi, e) != 1):
    print("Given values of n and e cannot be used for RSA Encryption.")
    print("Exiting...")
    exit(2)

d = findWholeNumberd(e, phi)
if(d == None):
    print("Given values of n and e cannot be used for RSA Encryption.")
    print("Exiting...")
    exit(3)
    
print(phi, d)
