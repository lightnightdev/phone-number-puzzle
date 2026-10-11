# Phone Number Puzzle
An answer to the puzzle posted by 3Blue1Brown  
[Link to original puzzle](https://www.youtube.com/shorts/ausLKMojXaY)

## Problem Statement

Given an integer $N$, find a multiplier $C$ such that $N \times C$ results in an integer consisting of only $1\text{s}$ and $0\text{s}$.  
e.g., Where $N=7$, $C=1442873$ and $7 \times 1442873 = 10100111$

## Mathematical Overview

The solution utilizes repeatings decimals of fractions to find an answer consisting of only $1\text{s}$ with $0\text{s}$ at the end to account for $2\text{s}$ and $5\text{s}$ as factors.

### **Repeating $1\text{s}$ and $\dfrac{1}{9}$**  
Assume that M is a number where $1/M$ has a cyclic repeating period. Multiples of $2$ and $5$ terminate, so we can take $N$ and factor out $2\text{s}$ and $5\text{s}$ to find the number that has a cyclic repeating period when dividing $1$ by it.

Because $1 = 0.\overline{9}$, the cyclic number making up the repeating period of $1/M$, when multiplied by M, returns all 9's.  
  
For example, in the case $N = 7$:  
$\dfrac{1}{7} = 0.\overline{142857}$ repeating, with $142857$ as the cyclic number.  
Then, $142857 \times 7 = 999999$, because it is essentially $\dfrac{1}{7} \times 7$, where the 9s repeat infinitely.  
  
Next, consider that  
$\dfrac{1}{9} = 0.\overline{1}$  
We can multiply $\dfrac{1}{9}$ by $\dfrac{n}{n}$ to get $\dfrac{n}{9*n}$ which also consists of repeating 1s. That means:  $\dfrac{1}{9*n} \times n = 0.\overline{1}$
  
So, the repeating cyclic period of $\dfrac{1}{9*N}$ is an integer that when multiplies by $N$ returns repeating $1\text{s}$.

$N = M \times 2^a \times 5^b$  
$Z = 2^a \times 5^b$  
$M = \dfrac{N}{Z}$  
$X = \dfrac{1}{9 \times M}$  
$Y = 5^a \times 2^b$  
$C = X \times Y$  

## My Solution:

- Strip out all prime factors 2 and 5 from N to get M. Store the count of those factors so we can multiply then into $10\text{s}$ later.
- Find the period length of M
- Pre-allocate the RAM bytearray buffer for the digits of the repeating cycle
- Calculate the repeating cycle and write to disk
- Multiply by 5 per the count of 2s, and 2 per the count of 5s
- Verify that final number times X is all 1s and 0s  

## Code Reference
- `get_period_length(N)`: Removes factors of $2$ and $5$ from $N$ and finds the length of the repeating cyclic number.
- `save_repeating_digits(N, period_length, output_file)`: Allocates a RAM bytearray buffer to write the $1/N$ ASCII digits directly to binary disk storage.
- `multiply_large_file(input_path, output_path, N, chunk_size)`: Reads the large string read from disk from right to left by streaming byte chunks, multiplies by N and manages the carry, and writes the answer back to disk.
- `read_and_print(input_path, digits)`: Streams and verifies output chunks to ensure pattern correctness.   