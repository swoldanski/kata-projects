# Kata03: How Big? How Fast?

Source: http://codekata.com/kata/kata03-how-big-how-fast/

## Problem

Rough estimation is a useful talent to possess. As you're coding away, you may suddenly need to work out approximately how big a data structure will be, or how fast some loop will run. The faster you can do this, the less the coding flow will be disturbed.

So this is a simple kata: a series of questions, each asking for a rough answer. Try to work each out in your head.

---

## How Big?

1. **Bits for unsigned representation** — roughly how many binary digits (bits) are required for:
   - 1,000
   - 1,000,000
   - 1,000,000,000
   - 1,000,000,000,000
   - 8,000,000,000,000

2. **Town records** — My town has approximately 20,000 residences. How much space is required to store the names, addresses, and a phone number for all of these (if we store them as characters)?

3. **Binary tree** — I'm storing 1,000,000 integers in a binary tree. Roughly how many nodes and levels can I expect the tree to have? Roughly how much space will it occupy on a 32-bit architecture?

---

## How Fast?

4. **Modem transfer** — My copy of Meyer's Object Oriented Software Construction has about 1,200 body pages. Assuming no flow control or protocol overhead, about how long would it take to send it over an async 56k baud modem line?

5. **Binary search scaling** — My binary search algorithm takes about 4.5ms to search a 10,000 entry array, and about 6ms to search 100,000 elements. How long would I expect it to take to search 10,000,000 elements (assuming I have sufficient memory to prevent paging)?

6. **Password cracking** — Unix passwords are stored using a one-way hash function: the original string is converted to the 'encrypted' password string, which cannot be converted back to the original string. One way to attack the password file is to generate all possible cleartext passwords, applying the password hash to each in turn and checking to see if the result matches the password you're trying to crack.

   In our particular system, passwords can be up to 16 characters long, and there are 96 possible characters at each position. If it takes 1ms to generate the password hash, is this a viable approach to attacking a password?

---

## Examples

```python
# Rough estimation examples (work in your head)

# Bits for 1,000,000
# log2(1,000,000) ≈ 20 bits

# Town records: 20,000 residences × ~100 chars = ~2 MB

# Binary tree: 1M nodes ≈ 20 levels, ~24 MB on 32-bit
```

## Goal

Practice rough estimation skills. Work each out in your head — no calculators, no writing code. The point is to develop intuition for orders of magnitude.