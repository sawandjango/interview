"""
LeetCode Problem #200: Number of Islands

Difficulty: Medium
Topics: Array, DFS, BFS, Matrix, Union Find
Companies: Amazon, Facebook, Google, Microsoft, Bloomberg, Apple, Uber


https://www.youtube.com/watch?v=ZgCZfXPo3hI&t=21s

================================================================================
                    📚 QUICK REFERENCE - WHAT'S IN THIS FILE
================================================================================

┌─────────────────────────────────────────────────────────────────────────────┐
│                        📖 TABLE OF CONTENTS                                 │
├──────┬──────────────────────────────────────┬───────────────────────────────┤
│ #    │ SECTION                              │ WHAT YOU'LL LEARN             │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 1    │ 🎯 PROBLEM UNDERSTANDING             │ • What is being asked?        │
│      │                                      │ • Real-world analogies        │
│      │                                      │ • Visual examples             │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 2    │ 🧠 KEY INSIGHTS TO REMEMBER          │ • Main challenge              │
│      │                                      │ • Base cases to handle        │
│      │                                      │ • Pattern recognition         │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 3    │ 🚀 HOW TO APPROACH THIS PROBLEM      │ • Step-by-step process        │
│      │                                      │ • Decision tree               │
│      │                                      │ • Interview scenarios         │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 4    │ 💡 SOLUTION 1: DFS (Recursive) ⭐     │ • WHY choose? (Pros/Cons)     │
│      │    (RECOMMENDED)                     │ • WHEN to use?                │
│      │                                      │ • Step-by-step walkthrough    │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 5    │ 💡 SOLUTION 2: BFS with Queue        │ • WHY choose? (Pros/Cons)     │
│      │    (Alternative)                     │ • WHEN to use?                │
│      │                                      │ • Comparison with Solution 1  │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 6    │ 💻 IMPLEMENTATION                    │ • Clean, commented code       │
│      │                                      │ • Both solutions              │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 7    │ 🧪 TEST CASES                        │ • Comprehensive tests         │
│      │                                      │ • Edge cases covered          │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 8    │ 🎓 LEARNING SUMMARY                  │ • Key takeaways               │
│      │                                      │ • Memory tricks               │
│      │                                      │ • Common mistakes             │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 9    │ 🔗 RELATED PROBLEMS                  │ • Similar problems            │
│      │                                      │ • Pattern recognition         │
└──────┴──────────────────────────────────────┴───────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                           🎯 MEMORY CHEAT SHEET                             │
├─────────────────────────────────────────────────────────────────────────────┤
│ ANALOGY          │ "Sink the Island" - Mark visited land as water!         │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ PATTERN          │ "Flood Fill" - Spread to all 4 neighbors (no diagonal!) │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ BASE CASE        │ Out of bounds OR water → Return                         │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ DEFAULT SOLUTION │ DFS Recursive (Use in 90% of cases!)                   │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ TIME COMPLEXITY  │ O(M×N) - Visit each cell at most once                  │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ SPACE COMPLEXITY │ O(M×N) - Recursion depth in worst case (all land)      │
└──────────────────┴─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                        ⚡ QUICK DECISION TABLE                              │
├────────────────────────────────┬────────────────────────────────────────────┤
│ SITUATION                      │ WHICH SOLUTION TO USE?                    │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Normal interview               │ ✅ Solution 1 (DFS Recursive)             │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Want simplest code             │ ✅ Solution 1 (Most intuitive)            │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Large grid (risk overflow)     │ ⚠️  Solution 2 (BFS avoids deep stack)    │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Need explicit control          │ ⚠️  Solution 2 (BFS with queue)           │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Want to show off               │ 🎯 Write Sol 1, then mention Sol 2       │
└────────────────────────────────┴────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                     📊 SOLUTION COMPARISON TABLE                            │
├──────────────────┬─────────────────────────┬────────────────────────────────┤
│ CRITERIA         │ SOLUTION 1 (DFS)        │ SOLUTION 2 (BFS Queue)        │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Code Length      │ ⭐⭐⭐⭐⭐ Very short     │ ⭐⭐⭐ More code                │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Readability      │ ⭐⭐⭐⭐⭐ Crystal clear  │ ⭐⭐⭐⭐ Clear                  │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Interview Speed  │ ⭐⭐⭐⭐⭐ Lightning fast │ ⭐⭐⭐ Takes longer             │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Stack Safety     │ ⭐⭐⭐ Deep recursion    │ ⭐⭐⭐⭐⭐ No stack overflow     │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Intuitiveness    │ ⭐⭐⭐⭐⭐ Very natural   │ ⭐⭐⭐⭐ Also intuitive         │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ When to Use      │ 90% of cases (DEFAULT)  │ Very large grids only         │
└──────────────────┴─────────────────────────┴────────────────────────────────┘

⏱️  TIME TO MASTER: 20-25 minutes
🎯 DIFFICULTY: Medium
💡 TIP: Remember "Sink the Island" - mark visited cells as water!
🔥 POPULAR: One of THE most common graph/matrix questions!

================================================================================
                           🎯 PROBLEM UNDERSTANDING
================================================================================

WHAT IS THE PROBLEM?
--------------------
Imagine you're looking at a MAP from above! Some parts are LAND ('1') and some
are WATER ('0'). You need to COUNT how many separate islands exist!

REAL WORLD ANALOGY:
------------------
Think of it like looking at a MINECRAFT world from above:
- '1' = Land blocks (grass, dirt)
- '0' = Water blocks (ocean, river)
- Island = Connected land pieces (up, down, left, right - NO diagonals!)

Your job: Count the number of separate islands!

Example Map:
```
1 1 0 0 0     [Land][Land][Water][Water][Water]
1 1 0 0 0     [Land][Land][Water][Water][Water]
0 0 1 0 0     [Water][Water][Land][Water][Water]
0 0 0 1 1     [Water][Water][Water][Land][Land]
```
Answer: 3 islands!
- Island 1: Top-left 2x2 block
- Island 2: Middle single cell
- Island 3: Bottom-right 2-cell piece

================================================================================
                            📝 FORMAL PROBLEM
================================================================================

Given an m x n 2D binary grid which represents a map of '1's (land) and
'0's (water), return the number of islands.

An island is surrounded by water and is formed by connecting adjacent lands
horizontally or vertically. You may assume all four edges of the grid are
surrounded by water.

Example 1:
----------
Input: grid = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
]
Output: 1

Visual:
🟩🟩🟩🟩🟦
🟩🟩🟦🟩🟦
🟩🟩🟦🟦🟦
🟦🟦🟦🟦🟦
(Only 1 connected island)

Example 2:
----------
Input: grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]
Output: 3

Visual:
🟩🟩🟦🟦🟦   ← Island 1
🟩🟩🟦🟦🟦   ← Island 1
🟦🟦🟩🟦🟦   ← Island 2
🟦🟦🟦🟩🟩   ← Island 3

Constraints:
------------
* m == grid.length
* n == grid[i].length
* 1 <= m, n <= 300
* grid[i][j] is '0' or '1'.

================================================================================
                         🧠 KEY INSIGHTS TO REMEMBER
================================================================================

THE MAIN CHALLENGE:
------------------
❌ Can't just count all '1's - they might be connected!
❌ Need to mark visited cells to avoid counting twice!
✅ When you find a '1', explore ALL connected '1's and count as ONE island!

THE MAGIC TRICK: "Sink the Island!"
-----------------------------------
Think of it like FLOOD FILLING:
1. Walk through the grid cell by cell
2. When you find LAND ('1'):
   - Count it as a new island (count++)
   - "SINK" the entire island (mark all connected '1's as visited)
   - Continue searching for more islands

How to SINK an island?
- Use DFS or BFS to visit all connected '1's
- Mark them as '0' or 'visited' so you don't count them again!

================================================================================
                          💡 SOLUTION APPROACHES
================================================================================
"""

# ============================================================================
#                    APPROACH 1: DFS (RECURSIVE) - MOST INTUITIVE
# ============================================================================

def numIslands_DFS(grid):
    """
    🎯 APPROACH 1: DFS - "Sink the Island" Strategy

    TIME COMPLEXITY: O(m × n) - Visit each cell once
    SPACE COMPLEXITY: O(m × n) - Recursion stack in worst case

    🧠 MEMORIZATION TRICK: "Find Land, Sink Island"
    -----------------------------------------------
    1. Loop through every cell
    2. Found land ('1')? That's a NEW island!
       - Increment counter
       - Sink the ENTIRE island (DFS to mark all connected land)
    3. Continue searching

    📝 STEP-BY-STEP ALGORITHM:
    --------------------------
    1. Initialize island_count = 0
    2. For each cell in grid:
       - If cell is '1' (land):
         * island_count++
         * DFS to sink entire island (mark all connected '1's as '0')
    3. Return island_count

    Why it works:
    - First '1' of each island triggers count++
    - DFS marks all connected land, so same island won't be counted again
    """
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    island_count = 0

    def dfs(r, c):
        """
        Sink the island starting from position (r, c)
        Mark all connected land as water ('0')
        """
        # Base cases: out of bounds or water
        if (r < 0 or r >= rows or
            c < 0 or c >= cols or
            grid[r][c] == '0'):
            return

        # Mark current land as visited (sink it!)
        grid[r][c] = '0'

        # Explore all 4 directions (up, down, left, right)
        dfs(r + 1, c)  # Down
        dfs(r - 1, c)  # Up
        dfs(r, c + 1)  # Right
        dfs(r, c - 1)  # Left

    # Scan the entire grid
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':  # Found land!
                island_count += 1   # New island found!
                dfs(r, c)           # Sink the entire island

    return island_count


# ============================================================================
#                    APPROACH 2: BFS (ITERATIVE) - LEVEL BY LEVEL
# ============================================================================

def numIslands_BFS(grid):
    """
    🎯 APPROACH 2: BFS - "Flood Fill" Strategy

    TIME COMPLEXITY: O(m × n) - Visit each cell once
    SPACE COMPLEXITY: O(min(m, n)) - Queue size in worst case

    🧠 MEMORIZATION TRICK: "Breadth-First Flooding"
    -----------------------------------------------
    Same idea as DFS, but use a QUEUE instead of recursion
    - Add starting land cell to queue
    - Process queue: mark cell as water, add neighbors
    - Continue until entire island is sunk

    📝 STEP-BY-STEP ALGORITHM:
    --------------------------
    1. Initialize island_count = 0
    2. For each cell in grid:
       - If cell is '1' (land):
         * island_count++
         * BFS to sink entire island using queue
    3. Return island_count
    """
    if not grid or not grid[0]:
        return 0

    from collections import deque

    rows, cols = len(grid), len(grid[0])
    island_count = 0

    def bfs(r, c):
        """
        Sink the island starting from position (r, c) using BFS
        """
        queue = deque([(r, c)])
        grid[r][c] = '0'  # Mark as visited

        # Directions: up, down, left, right
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        while queue:
            curr_r, curr_c = queue.popleft()

            # Check all 4 neighbors
            for dr, dc in directions:
                new_r, new_c = curr_r + dr, curr_c + dc

                # Valid land cell?
                if (0 <= new_r < rows and
                    0 <= new_c < cols and
                    grid[new_r][new_c] == '1'):

                    queue.append((new_r, new_c))
                    grid[new_r][new_c] = '0'  # Mark as visited

    # Scan the entire grid
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':  # Found land!
                island_count += 1   # New island found!
                bfs(r, c)           # Sink the entire island

    return island_count


# ============================================================================
#              APPROACH 3: DFS with Visited Set (Non-Destructive)
# ============================================================================

def numIslands_DFS_Visited(grid):
    """
    🎯 APPROACH 3: DFS with Visited Set (Don't modify original grid)

    TIME COMPLEXITY: O(m × n)
    SPACE COMPLEXITY: O(m × n) - For visited set + recursion

    Use this if you can't modify the input grid!
    """
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    visited = set()
    island_count = 0

    def dfs(r, c):
        """Explore island starting from (r, c)"""
        if (r < 0 or r >= rows or
            c < 0 or c >= cols or
            grid[r][c] == '0' or
            (r, c) in visited):
            return

        visited.add((r, c))

        # Explore all 4 directions
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1' and (r, c) not in visited:
                island_count += 1
                dfs(r, c)

    return island_count


# ============================================================================
#                    🎨 VISUAL WALKTHROUGH EXAMPLE
# ============================================================================

"""
Let's walk through Example 2: 3 Islands

Original Grid:
    0   1   2   3   4
0  [1] [1]  0   0   0
1  [1] [1]  0   0   0
2   0   0  [1]  0   0
3   0   0   0  [1] [1]

STEP-BY-STEP DFS EXECUTION:
---------------------------

Step 1: Scan grid, find first '1' at (0,0)
   - island_count = 1
   - Start DFS from (0,0)
   - Sink connected land:

   DFS from (0,0):
   ├─ Visit (0,0) → mark as '0'
   ├─ Go down to (1,0)
   │  ├─ Visit (1,0) → mark as '0'
   │  ├─ Go down to (2,0) → water, stop
   │  ├─ Go up to (0,0) → already '0', stop
   │  ├─ Go right to (1,1)
   │  │  ├─ Visit (1,1) → mark as '0'
   │  │  └─ ... (all neighbors are water/visited)
   │  └─ Go left to (1,-1) → out of bounds
   ├─ Go right to (0,1)
   │  ├─ Visit (0,1) → mark as '0'
   │  └─ ... (all neighbors handled)
   └─ All land connected to (0,0) is now sunk!

   Grid after sinking Island 1:
      0   1   2   3   4
   0  0   0   0   0   0
   1  0   0   0   0   0
   2  0   0  [1]  0   0
   3  0   0   0  [1] [1]

Step 2: Continue scanning, find '1' at (2,2)
   - island_count = 2
   - Start DFS from (2,2)
   - Sink this single cell

   Grid after sinking Island 2:
      0   1   2   3   4
   0  0   0   0   0   0
   1  0   0   0   0   0
   2  0   0   0   0   0
   3  0   0   0  [1] [1]

Step 3: Continue scanning, find '1' at (3,3)
   - island_count = 3
   - Start DFS from (3,3)
   - Sink connected land (3,3) and (3,4)

   Grid after sinking Island 3:
      0   1   2   3   4
   0  0   0   0   0   0
   1  0   0   0   0   0
   2  0   0   0   0   0
   3  0   0   0   0   0

Step 4: Grid fully scanned, all water
   - Final answer: island_count = 3 ✓
"""

# ============================================================================
#              🎯 MEMORY TRICKS & COMMON MISTAKES
# ============================================================================

"""
🧠 HOW TO REMEMBER THIS SOLUTION:
---------------------------------
Analogy: "FLOOD DETECTION"
1. Walk through the map cell by cell
2. See land? You found a NEW FLOOD!
   - Count it (+1)
   - FLOOD the entire area (DFS/BFS)
   - Mark all connected land as water
3. Keep searching for more floods

Simple Mantra: "Find, Count, Flood, Repeat"

❌ COMMON MISTAKES TO AVOID:
----------------------------
1. ❌ Forgetting to mark cells as visited
      → Infinite loops and wrong count!

2. ❌ Counting '1's instead of islands
      → Wrong! Need to count CONNECTED components!

3. ❌ Forgetting boundary checks
      → Array index out of bounds!

4. ❌ Using 8 directions (including diagonals)
      → Problem says only 4 directions (up/down/left/right)!

5. ❌ Not handling edge cases (empty grid)
      → Crashes!

✅ PRO TIPS:
-----------
1. DFS is more intuitive (recursion feels natural)
2. BFS uses more space but is iterative
3. Always mark as visited BEFORE recursive calls
4. Remember: Only 4 directions, NO diagonals!
5. Grid modification is OK here (makes it simpler)
"""

# ============================================================================
#                         🧪 TEST CASES
# ============================================================================

def test_numIslands():
    """Run comprehensive test cases"""

    print("="*70)
    print("              NUMBER OF ISLANDS - TEST CASES")
    print("="*70)

    # Test Case 1: Single large island
    print("\n📝 Test Case 1: Single large island")
    print("-" * 70)
    grid1 = [
        ["1","1","1","1","0"],
        ["1","1","0","1","0"],
        ["1","1","0","0","0"],
        ["0","0","0","0","0"]
    ]
    print("Grid:")
    for row in grid1:
        print("  " + " ".join(row))

    # Make a copy for each method
    import copy
    grid1_copy1 = copy.deepcopy(grid1)
    grid1_copy2 = copy.deepcopy(grid1)
    grid1_copy3 = copy.deepcopy(grid1)

    result1_dfs = numIslands_DFS(grid1_copy1)
    result1_bfs = numIslands_BFS(grid1_copy2)
    result1_visited = numIslands_DFS_Visited(grid1_copy3)

    print(f"\nDFS Result: {result1_dfs}")
    print(f"BFS Result: {result1_bfs}")
    print(f"Visited Set Result: {result1_visited}")
    print(f"Expected: 1")
    print(f"✓ PASS" if result1_dfs == 1 else "✗ FAIL")

    # Test Case 2: Three islands
    print("\n📝 Test Case 2: Three separate islands")
    print("-" * 70)
    grid2 = [
        ["1","1","0","0","0"],
        ["1","1","0","0","0"],
        ["0","0","1","0","0"],
        ["0","0","0","1","1"]
    ]
    print("Grid:")
    for row in grid2:
        print("  " + " ".join(row))

    grid2_copy = copy.deepcopy(grid2)
    result2 = numIslands_DFS(grid2_copy)
    print(f"\nResult: {result2}")
    print(f"Expected: 3")
    print(f"✓ PASS" if result2 == 3 else "✗ FAIL")

    # Test Case 3: All water
    print("\n📝 Test Case 3: All water (no islands)")
    print("-" * 70)
    grid3 = [
        ["0","0","0"],
        ["0","0","0"]
    ]
    print("Grid:")
    for row in grid3:
        print("  " + " ".join(row))

    grid3_copy = copy.deepcopy(grid3)
    result3 = numIslands_DFS(grid3_copy)
    print(f"\nResult: {result3}")
    print(f"Expected: 0")
    print(f"✓ PASS" if result3 == 0 else "✗ FAIL")

    # Test Case 4: All land
    print("\n📝 Test Case 4: All land (one big island)")
    print("-" * 70)
    grid4 = [
        ["1","1","1"],
        ["1","1","1"]
    ]
    print("Grid:")
    for row in grid4:
        print("  " + " ".join(row))

    grid4_copy = copy.deepcopy(grid4)
    result4 = numIslands_DFS(grid4_copy)
    print(f"\nResult: {result4}")
    print(f"Expected: 1")
    print(f"✓ PASS" if result4 == 1 else "✗ FAIL")

    # Test Case 5: Complex pattern
    print("\n📝 Test Case 5: Complex zigzag pattern")
    print("-" * 70)
    grid5 = [
        ["1","0","1","0","1"],
        ["0","1","0","1","0"],
        ["1","0","1","0","1"]
    ]
    print("Grid:")
    for row in grid5:
        print("  " + " ".join(row))

    grid5_copy = copy.deepcopy(grid5)
    result5 = numIslands_DFS(grid5_copy)
    print(f"\nResult: {result5}")
    print(f"Expected: 9 (each '1' is separate)")
    print(f"✓ PASS" if result5 == 9 else "✗ FAIL")

    print("\n" + "="*70)
    print("              ✅ ALL TEST CASES COMPLETED!")
    print("="*70)


if __name__ == "__main__":
    test_numIslands()


# ============================================================================
#              🎓 LEARNING SUMMARY & KEY TAKEAWAYS
# ============================================================================

"""
🎯 WHAT YOU LEARNED:
-------------------
1. Island counting = Connected Component counting
2. DFS/BFS both work - "sink" strategy is key
3. Mark visited cells to avoid double counting
4. Only 4 directions matter (no diagonals)

🔑 KEY PATTERN: "Find & Flood"
------------------------------
This pattern applies to:
- Number of Islands (this problem)
- Max Area of Island
- Surrounded Regions
- Flood Fill
- Pacific Atlantic Water Flow

💪 SIMILAR PROBLEMS TO PRACTICE:
-------------------------------
1. LeetCode #695: Max Area of Island (find largest island)
2. LeetCode #463: Island Perimeter (calculate perimeter)
3. LeetCode #130: Surrounded Regions (flip surrounded areas)
4. LeetCode #733: Flood Fill (paint connected pixels)
5. LeetCode #417: Pacific Atlantic Water Flow

🎉 CONGRATULATIONS!
------------------
You now understand the "Find & Flood" pattern!
Remember: "Find Land → Count Island → Flood/Sink → Repeat!"

Key Differences from Clone Graph:
- Clone Graph: Need HashMap to track old→new mapping
- Number of Islands: Just need to COUNT and MARK visited
"""
