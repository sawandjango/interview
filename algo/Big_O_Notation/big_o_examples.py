"""
Big O Notation - Time Complexity Examples
==========================================

WHAT IS BIG O NOTATION?
-----------------------
Big O notation is a mathematical way to describe how the runtime or space requirements
of an algorithm grow as the input size increases. It focuses on the worst-case scenario
and ignores constants and lower-order terms.

WHY IS IT IMPORTANT?
--------------------
1. PERFORMANCE PREDICTION: Helps predict how your code will perform with large datasets
   - An O(n²) algorithm with 1000 items = 1,000,000 operations
   - An O(n) algorithm with 1000 items = 1,000 operations

2. INTERVIEW SUCCESS: Critical for technical interviews at top companies
   - Interviewers expect you to analyze and optimize time/space complexity
   - Differentiates between junior and senior developers

3. SCALABILITY: Ensures your code works efficiently as data grows
   - What works for 100 users might crash with 1,000,000 users
   - Helps choose the right algorithm/data structure for the problem

4. OPTIMIZATION: Identifies bottlenecks before they become problems
   - Compare different approaches objectively
   - Make informed trade-offs between time and space

BASIC CONCEPTS:
--------------
- n = size of input (e.g., array length, number of elements)
- We care about GROWTH RATE, not exact operations
- Drop constants: O(2n) → O(n), O(500) → O(1)
- Keep dominant term: O(n² + n) → O(n²)
- Worst case scenario is typically analyzed

REAL-WORLD ANALOGY:
------------------
Think of looking up a name in a phone book:
- O(1): You know the exact page number → Direct access
- O(log n): You open middle, eliminate half each time → Binary search
- O(n): You check every page from start → Linear search
- O(n²): You compare every name with every other name → Nested loops

Understanding how algorithm efficiency scales with input size.
"""

# O(1) - Constant Time
# Time doesn't increase with input size
def constant_time_example(arr):
    """Always takes same time regardless of array size"""
    if len(arr) > 0:
        return arr[0]  # Accessing first element
    return None

# Example: constant_time_example([1,2,3,4,5]) -> Always 1 operation


# O(log n) - Logarithmic Time
# Time increases logarithmically (dividing problem in half each time)
def binary_search(arr, target):
    """Searching in sorted array by halving search space"""
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# Example: binary_search([1,2,3,4,5,6,7,8], 6)
# n=8 -> max 3 iterations (log₂8 = 3)


# O(n) - Linear Time
# Time increases proportionally with input size
def linear_time_example(arr):
    """Must check every element once"""
    total = 0
    for num in arr:
        total += num
    return total

# Example: linear_time_example([1,2,3,4,5])
# n=5 -> 5 operations, n=100 -> 100 operations


# O(n log n) - Linearithmic Time
# Common in efficient sorting algorithms
def merge_sort(arr):
    """Divides array (log n) and merges (n) at each level"""
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

# Example: merge_sort([5,2,8,1,9])
# Divides log n times, merges n elements at each level


# O(n²) - Quadratic Time
# Nested loops over the same data
def quadratic_time_example(arr):
    """Comparing each element with every other element"""
    pairs = []
    for i in range(len(arr)):
        for j in range(len(arr)):
            pairs.append((arr[i], arr[j]))
    return pairs

# Example: quadratic_time_example([1,2,3])
# n=3 -> 9 operations (3²), n=100 -> 10,000 operations


# O(2ⁿ) - Exponential Time
# Time doubles with each additional input element
def fibonacci_recursive(n):
    """Recursive fibonacci without memoization"""
    if n <= 1:
        return n
    return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)

# Example: fibonacci_recursive(5)
# Creates tree of recursive calls: 2⁵ = 32 operations
# fibonacci_recursive(10) -> 2¹⁰ = 1024 operations


# O(n!) - Factorial Time
# Generating all permutations
def generate_permutations(arr):
    """All possible orderings of elements"""
    if len(arr) <= 1:
        return [arr]

    perms = []
    for i in range(len(arr)):
        rest = arr[:i] + arr[i+1:]
        for perm in generate_permutations(rest):
            perms.append([arr[i]] + perm)
    return perms

# Example: generate_permutations([1,2,3])
# n=3 -> 6 permutations (3! = 6)
# n=4 -> 24 permutations (4! = 24)
# n=10 -> 3,628,800 permutations (10!)


# Space Complexity Examples
# -------------------------

# O(1) Space - Constant Space
def constant_space(arr):
    """Only uses fixed amount of extra memory"""
    total = 0  # Single variable
    for num in arr:
        total += num
    return total


# O(n) Space - Linear Space
def linear_space(n):
    """Creates array proportional to input"""
    return [i for i in range(n)]


# O(n²) Space - Quadratic Space
def quadratic_space(n):
    """Creates 2D matrix"""
    return [[0 for _ in range(n)] for _ in range(n)]


# Common Complexity Rankings (Best to Worst)
# -------------------------------------------
# O(1)       < Constant
# O(log n)   < Logarithmic
# O(n)       < Linear
# O(n log n) < Linearithmic
# O(n²)      < Quadratic
# O(2ⁿ)      < Exponential
# O(n!)      < Factorial


if __name__ == "__main__":
    # Test examples
    print("O(1) Constant:", constant_time_example([1,2,3,4,5]))
    print("O(log n) Binary Search:", binary_search([1,2,3,4,5,6,7,8], 6))
    print("O(n) Linear:", linear_time_example([1,2,3,4,5]))
    print("O(n log n) Merge Sort:", merge_sort([5,2,8,1,9]))
    print("O(n²) Quadratic pairs count:", len(quadratic_time_example([1,2,3])))
    print("O(2ⁿ) Fibonacci(10):", fibonacci_recursive(10))
    print("O(n!) Permutations of [1,2,3]:", len(generate_permutations([1,2,3])))
