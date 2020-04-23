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

print('''
Usage: 

1. Unencrypted data must be entered as text.
2. Ciphertext must be decimal encoded.
''')


#used to compare if a number is a whole number
def truncate(num):
    return int((num * 1000000)/1000000)

#Returns list of prime factors of a given number
def primeFactors(number):
    i = 2
    factors = []
    while i * i <= number:
        if number % i:
            i += 1
        else:
            number //= i
            factors.append(i)
    if number > 1:
        factors.append(number)
    return factors

#returns list of elements with no duplicates
def removeDuplicates(primeFactorList):
    finalList = []
    for i in primeFactorList:
        if i not in finalList:
            finalList.append(i)
    return finalList

#finds the private key number d in the RSA Algorithm
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

print('\n \n')

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
    
print('Smaller prime p:', p)
print('Larger prime q:', q)
print('Public Key (e, n): ({0}, {1})'.format(e, n))
print('Private Key (d, n): ({0}, {1})'.format(int(d), n))

print('\n \n')

#decoding cipher text
print('Decode ciphertext ONLY into coressponding numeric counterparts. Input MUST be numeric.')
check = input('Do you want to decode a string? (y/n):  ')
if (check == 'y') or (check == 'Y'):
    cipherText = input('Enter encoded numbers separated by a space: ')
    cipherTextList = cipherText.split(' ')
    messageTextList = []
    #formula to decrypt
    for i in cipherTextList:
        decrypted = (int(i)**d) % n
        messageTextList.append(decrypted)
    print('Decoded list:', messageTextList)
else:
    exit(0)


