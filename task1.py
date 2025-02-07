import sys
import math

# Function to compute nth Catalan number
def catalan_number(n):
    return math.comb(2 * n, n) // (n + 1)

# Precompute Catalan numbers for n up to 30
max_n = 30
catalan = [catalan_number(i) for i in range(max_n + 1)]

# Read input
t = int(sys.stdin.readline().strip())  # Number of test cases
results = []

for _ in range(t):
    n = int(sys.stdin.readline().strip())  # Number of chits
    results.append(str(catalan[n]))  # Store results as string

# Print all results at once for efficiency
print("\n".join(results))
