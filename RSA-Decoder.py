import argparse
from math import gcd, isqrt
import sys
from typing import List

# Helper functions

def is_prime(num) -> bool:
    """Checks if a number is prime."""
    if num < 2:
        return False
    for i in range(2, isqrt(num) + 1):
        if num % i == 0:
            return False
    return True

def truncate(num) -> int:
    """Used to compare if a number is a whole number."""
    return int((num * 10000000)/10000000)

def prime_factors(number: int) -> List[int]:
    """Returns a list of prime factors of a given number."""
    i = 2
    factors = []
    # Optimization: only check up to sqrt(number)
    while i * i <= number:
        if number % i == 0:
            number //= i
            factors.append(i)
        else:
            i += 1
    # If number is still > 1, it must be a prime factor itself
    if number > 1:
        factors.append(number)
    return factors

def remove_duplicates(primeFactorList: List[int]) -> List[int]:
    """Returns list of elements with no duplicates."""
    finalList = []
    for i in primeFactorList:
        if i not in finalList:
            finalList.append(i)
    return finalList

def find_private_key_exponent(e: int, phi: int):
    """Finds the private key exponent D using the extended Euclidean algorithm implicitly."""
    # A more robust way is using modular inverse: pow(e, -1, phi)
    # But keeping original logic for now.
    # Increase range significantly, as d can be large
    # A better approach is needed for very large numbers, like Extended Euclidean Algorithm
    limit = phi * 2 # Heuristic limit, might need adjustment or a better algorithm
    for i in range(1, limit): # Start from 1, d can't be 0
        d_candidate = (1 + (i * phi)) / e
        # Check if it results in an integer and is positive
        if d_candidate > 0 and abs(d_candidate - round(d_candidate)) < 1e-10: # Tolerance for float issues
             # Further check if (e * int(round(d_candidate))) % phi == 1
             d_int = int(round(d_candidate))
             if (e * d_int) % phi == 1:
                 return d_int
    return None # Indicate failure to find d within the range

def rsa_encode(plaintext, e, n) -> List[int]:
    """Encodes a list of decimal numbers using RSA."""
    encoded_list = []
    print(f"\nEncoding using Public Key (e={e}, n={n})...")
    for p in plaintext:
        if p >= n:
            print(f"Warning: Message '{p}' is >= n '{n}'. RSA may not work correctly.", file=sys.stderr)
        # Calculate ciphertext c = p^e mod n
        c = pow(p, e, n)
        encoded_list.append(c)
    return encoded_list

def rsa_decode(ciphertext, d, n):
    """Decodes a list of cipher text numbers using RSA."""
    decoded_list = []
    print(f"\nDecoding using Private Key (d={d}, n={n})...")
    for c in ciphertext:
        if c >= n:
            print(f"Warning: Ciphertext '{c}' is >= n '{n}'. This may indicate an isue.", file=sys.stderr)
        # Calculate message m = c^d mod n
        m = pow(c, d, n)
        decoded_list.append(m)
    return decoded_list

def main():
    # --- Argument Parsing Setup ---
    parser = argparse.ArgumentParser(
        description='''RSA Key Discovery, Encoding, and Decoding Tool.

        Modes of Operation:
        1. Key Discovery & Decoding: Provide n and e to find p, q, d. Optionally provide ciphertext to decode.
           Example: python your_script.py -n 3233 -e 17 --decode 2790 1510 3039
        2. Encoding: Provide p, q, and e, along with decimals to encode.
           Example: python your_script.py -p 61 -q 53 -e 17 --encode 123 456 789
        ''',
        formatter_class=argparse.RawTextHelpFormatter # Preserves newlines in description
    )

    # Group for Key Discovery/Decoding Mode
    group1 = parser.add_argument_group('Key Discovery/Decoding Mode (requires n, e)')
    group1.add_argument('-n', type=int, help='The modulus n (product of two primes p*q)')
    group1.add_argument('-e', type=int, help='The public exponent e')
    group1.add_argument('--decode', type=int, nargs='+', # '+' means 1 or more arguments
                        help='Space-separated list of ciphertext numbers to decode.')

    # Group for Encoding Mode
    group2 = parser.add_argument_group('Encoding Mode (requires p, q, e, --encode)')
    group2.add_argument('-p', type=int, help='The first prime number p')
    group2.add_argument('-q', type=int, help='The second prime number q')
    # Note: -e is used by both modes, defined in group1 but usable here too if p,q are set
    group2.add_argument('--encode', type=int, nargs='+', # '+' means 1 or more arguments
                        help='Space-separated list of decimal numbers to encode.')

    args = parser.parse_args()

 # --- Input Validation and Mode Determination ---

    # Mode 1: Key Discovery / Decoding (n and e provided)
    if args.n is not None and args.e is not None:
        if args.p is not None or args.q is not None or args.encode is not None:
            parser.error("Cannot use -p, -q, or --encode when -n and -e are specified.")

        n = args.n
        e = args.e
        print(f"Received n = {n}, e = {e}")
        print("Attempting to find prime factors p and q from n...")

        primeFactorList = prime_factors(n)
        # Note: Original code used removeDuplicates, but primeFactors itself for RSA
        # should ideally return only two *distinct* primes. Let's refine this.
        distinct_factors = remove_duplicates(primeFactorList)

        if len(distinct_factors) != 2:
            print(f"Error: Value n={n} has {len(distinct_factors)} distinct prime factor(s): {distinct_factors}.", file=sys.stderr)
            print("RSA requires n to be the product of exactly two distinct prime numbers.", file=sys.stderr)
            print("Exiting...", file=sys.stderr)
            sys.exit(1)

        # Check if the factors found actually multiply back to n
        p_cand, q_cand = sorted(distinct_factors)
        if p_cand * q_cand != n:
             print(f"Error: Found factors {p_cand}, {q_cand} do not multiply to n={n}. Check factorization.", file=sys.stderr)
             sys.exit(1)

        # Check if p and q are actually prime (basic check)
        if not is_prime(p_cand) or not is_prime(q_cand):
            print(f"Error: Factors found ({p_cand}, {q_cand}) are not both prime numbers.", file=sys.stderr)
            sys.exit(1)

        p = p_cand
        q = q_cand
        print(f"Found primes: p = {p}, q = {q}")

        phi = (p - 1) * (q - 1)
        print(f"Calculated phi(n) = {phi}")

        if gcd(phi, e) != 1:
            print(f"Error: Public exponent e={e} is not coprime with phi={phi} (gcd={gcd(phi, e)}).", file=sys.stderr)
            print("These values cannot be used for RSA.", file=sys.stderr)
            print("Exiting...", file=sys.stderr)
            sys.exit(2)
        print(f"Verified: gcd(e, phi) = gcd({e}, {phi}) = 1")

        print("Calculating private exponent d...")
        d = find_private_key_exponent(e, phi)
        # Alternative using modular inverse (more robust)
        # try:
        #     d = pow(e, -1, phi)
        # except ValueError: # Happens if gcd(e, phi) != 1, but we already checked
        #     d = None

        if d is None:
            print(f"Error: Could not find the private exponent d for e={e} and phi={phi}.", file=sys.stderr)
            print("The find_private_key_exponent function might need adjustment or a different algorithm (like Extended Euclidean Algorithm) for these numbers.", file=sys.stderr)
            print("Exiting...", file=sys.stderr)
            sys.exit(3)

        print(f"\n--- RSA Key Information ---")
        print(f'Smaller prime p: {p}')
        print(f'Larger prime q:  {q}')
        print(f'Modulus n:       {n}')
        print(f'Phi(n):          {phi}')
        print(f'Public Key (e, n):  ({e}, {n})')
        print(f'Private Key (d, n): ({int(d)}, {n})') # d should be int

        # Perform decoding if requested
        if args.decode:
            print(f"\nReceived ciphertext to decode: {args.decode}")
            try:
                # Ensure d is integer for pow function
                decrypted_message = rsa_decode(args.decode, int(d), n)
                print(f"\n--- Decryption Result ---")
                print(f"Decoded message (numeric): {decrypted_message}")
            except Exception as err:
                print(f"\nError during decoding: {err}", file=sys.stderr)
                sys.exit(4)
        else:
             print("\nNo ciphertext provided for decoding.")


    # Mode 2: Encoding (p, q, e, and --encode provided)
    elif args.p is not None and args.q is not None and args.e is not None and args.encode is not None:
        if args.n is not None or args.decode is not None:
             parser.error("Cannot use -n or --decode when -p, -q, -e, and --encode are specified.")

        p = args.p
        q = args.q
        e = args.e
        message_decimals = args.encode

        print(f"Received primes p = {p}, q = {q}")
        print(f"Received public exponent e = {e}")
        print(f"Received decimals to encode: {message_decimals}")

        # Validate p and q
        if not is_prime(p) or not is_prime(q):
            print(f"Error: Provided p={p} or q={q} is not a prime number.", file=sys.stderr)
            sys.exit(1)
        if p == q:
            print(f"Error: Primes p and q must be distinct (p={p}, q={q}).", file=sys.stderr)
            sys.exit(1)

        n = p * q
        phi = (p - 1) * (q - 1)
        print(f"Calculated modulus n = p * q = {n}")
        print(f"Calculated phi(n) = (p-1)*(q-1) = {phi}")

        # Validate e
        if e <= 1 or e >= phi:
             print(f"Error: Public exponent e={e} must be 1 < e < phi={phi}.", file=sys.stderr)
             sys.exit(2)
        if gcd(phi, e) != 1:
            print(f"Error: Public exponent e={e} is not coprime with phi={phi} (gcd={gcd(phi, e)}).", file=sys.stderr)
            print("Cannot use this e for RSA encryption.", file=sys.stderr)
            sys.exit(2)
        print(f"Verified: gcd(e, phi) = gcd({e}, {phi}) = 1")

        # Perform encoding
        try:
            encoded_ciphertext = rsa_encode(message_decimals, e, n)
            print(f"\n--- Encoding Result ---")
            print(f"Public Key (e, n): ({e}, {n})")
            print(f"Original Decimals: {message_decimals}")
            print(f"Encoded Ciphertext: {encoded_ciphertext}")
        except Exception as err:
            print(f"\nError during encoding: {err}", file=sys.stderr)
            sys.exit(4)

    # Invalid combination or missing arguments
    else:
        # Check specific missing arguments for better messages
        if (args.p is not None or args.q is not None or args.encode is not None) and args.e is None:
             parser.error("Encoding mode requires -e (public exponent) along with -p, -q, and --encode.")
        elif (args.n is not None and args.e is None) or (args.e is not None and args.n is None):
             parser.error("Key Discovery/Decoding mode requires both -n and -e.")
        else:
             print("Error: Invalid combination of arguments or missing required arguments.", file=sys.stderr)
             print("Please provide either (-n and -e) or (-p, -q, -e, and --encode).", file=sys.stderr)
             parser.print_help()
             sys.exit(5)

# --- Entry Point ---
if __name__ == "__main__":
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
    main()
