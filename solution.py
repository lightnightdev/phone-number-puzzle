import os
import re
import time


def get_period_length(N: int) -> tuple[int, int, int]:
    """Returns the period length of 1/N."""
    if N <= 0:
        raise ValueError("N must be positive.")

    twos = 0
    fives = 0

    # Strip all factors of 2 and 5
    while N % 2 == 0:
        N //= 2
        twos += 1
    while N % 5 == 0:
        N //= 5
        fives += 1

    # If N's only factors are 2 and 5, then the decimal terminates
    if N == 1:
        return 0, twos, fives

    # Find smallest L such that (10**L % N) == 1
    rem = 10 % N
    L = 1
    while rem != 1:
        rem = (rem * 10) % N
        L += 1

    return L, twos, fives


def save_repeating_digits(N: int, period_length: int, output_file: str = "digits.txt"):
    print(f"Generating {period_length:,} digits for 1/{N}...")
    start_time = time.time()

    # Pre-allocate 82 MB buffer in RAM (48 is ASCII code for '0')
    buffer = bytearray(period_length)

    rem = 1
    for i in range(period_length):
        rem *= 10
        buffer[i] = (rem // N) + 48
        rem %= N

    # Write directly to disk as binary bytes
    with open(output_file, "wb") as f:
        f.write(buffer)

    elapsed = time.time() - start_time
    print(
        f"Done! Saved {period_length:,} digits (~{period_length / 1e6:.1f} MB) in {elapsed:.2f} seconds."
    )


def multiply_large_file(
    input_path: str, output_path: str, N: int, chunk_size: int = 1_000
):
    file_size = os.path.getsize(input_path)
    carry = 0
    chunks_out = []

    with open(input_path, "rb") as f_in:
        pos = file_size

        while pos > 0:
            read_len = min(chunk_size, pos)
            pos -= read_len

            f_in.seek(pos)
            chunk_bytes = f_in.read(read_len)

            # Multiply block: V = (Chunk * N) + Carry
            val = int(chunk_bytes) * N + carry

            modulus = 10**read_len
            carry = val // modulus
            remainder = val % modulus

            # Format remainder with exact chunk length to preserve leading zeros
            chunks_out.append(f"{remainder:0{read_len}d}".encode("ascii"))

    if carry > 0:
        chunks_out.append(str(carry).encode("ascii"))

    # Write output chunks in reverse order (most significant to least significant)
    with open(output_path, "wb") as f_out:
        f_out.writelines(reversed(chunks_out))

    print(f"Done multiplying file {output_path} by {N}")


def read_and_print(input_path, digits=250):
    with open(input_path, 'r') as infile:
        i = 0
        found_flag = 0
        while True:
            chunk = infile.read(digits)
            if not chunk:
                break
            if re.search(r'[^01]', chunk):
                found_flag += 1
                print(f"Line {i}", chunk)
            i += 1
        if found_flag > 0:
            print(f"Found {found_flag} lines ({digits} digits/line) with mismatches")
        print(f"Done checking {input_path}")

def process_n(n: int):
    l, a_twos, b_fives = get_period_length(9 * n)

    z = 2 ** (a_twos) * 5 ** (b_fives)
    m = n // z

    print(n, z, m)

    save_repeating_digits(9 * m, l)

    y = 5 ** (a_twos) * 2 ** (b_fives)
    multiply_large_file("digits.txt", "digits_2.txt", y)

    multiply_large_file("digits_2.txt", "dense_output.txt", n)

    read_and_print("dense_output.txt")



if __name__ == "__main__":
    process_n(31415926535)