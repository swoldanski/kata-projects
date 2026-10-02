# Alphabet Cipher

Source: https://github.com/gigasquid/wonderland-clojure-katas/tree/master/alphabet-cipher

## Problem

Implement a simple substitution cipher based on a keyword. This is a classic cryptography exercise.

## Description

The cipher uses a keyword to generate a substitution alphabet:
1. Write the keyword (removing duplicate letters)
2. Append the remaining letters of the alphabet in order
3. Map each plaintext letter to the corresponding cipher letter

## Example

Keyword: `CIPHER`

```
Plain:  A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
Cipher: C I P H E R A B D F G J K L M N O Q S T U V W X Y Z
```

## Goals

- Generate cipher alphabet from keyword
- Encrypt/decrypt messages
- Handle case preservation
- Handle non-alphabetic characters
- Support different alphabets (ASCII, Unicode)

## Exercises

1. Basic encryption/decryption
2. Keyword validation and normalization
3. Frequency analysis attack
4. Support for spaces/punctuation
5. Vigenère cipher extension (polyalphabetic)