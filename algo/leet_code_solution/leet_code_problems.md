# Top 100 Important LeetCode Problems - Visual Diagram Guide

---

## MAIN CLASSIFICATION

```
                        TOP 100 LEETCODE PROBLEMS
                                   |
        ┌──────────────┬───────────┼──────────┬────────────┬──────────────┐
        |              |           |          |            |              |
        ↓              ↓           ↓          ↓            ↓              ↓
  ARRAY/STRING    LINKED LIST   TREE/GRAPH  STACK/QUEUE  HASH TABLE   HEAP/PQ
   (30 probs)     (10 probs)    (25 probs)  (8 probs)    (8 probs)    (5 probs)
```

---

## COMPLETE PROBLEM LIST BY DATA STRUCTURE

```
┌─────────────────────────┬─────────────────────────┬─────────────────────────┬─────────────────────────┐
│   ARRAY/STRING (30)     │   LINKED LIST (10)      │   TREE/GRAPH (25)       │   STACK/QUEUE (8)       │
├─────────────────────────┼─────────────────────────┼─────────────────────────┼─────────────────────────┤
│                         │                         │                         │                         │
│ EASY (7):               │ EASY (4):               │ EASY (5):               │ EASY (2):               │
│  1. Two Sum             │  31. Reverse LL         │  41. Max Depth BT       │  66. Valid Parentheses  │
│  2. Buy/Sell Stock      │  32. Merge Two Lists    │  42. Same Tree          │  67. Queue using Stack  │
│  3. Contains Duplicate  │  33. LL Cycle           │  43. Invert BT          │                         │
│  4. Valid Palindrome    │  34. Palindrome LL      │  44. Symmetric Tree     │ MEDIUM (4):             │
│  5. Maximum Subarray    │                         │  45. BT Level Order     │  68. Min Stack          │
│  6. Merge Sorted Array  │ MEDIUM (5):             │                         │  69. Eval RPN           │
│  7. Plus One            │  35. Add Two Numbers    │ MEDIUM (15):            │  70. Daily Temps        │
│                         │  36. Remove Nth Node    │  46. Validate BST       │  71. Car Fleet          │
│ MEDIUM (17):            │  37. Reorder List       │  47. BT Inorder         │                         │
│  8. 3Sum                │  38. LL Cycle II        │  48. BT Zigzag          │ HARD (2):               │
│  9. Container Water     │  39. Copy Random Ptr    │  49. Construct BT       │  72. Largest Rectangle  │
│  10. Product Array      │                         │  50. LCA of BST         │  73. Sliding Window Max │
│  11. Longest Substring  │ HARD (1):               │  51. Kth Smallest BST   │                         │
│  12. Longest Palindrome │  40. Merge K Lists      │  52. Number of Islands  │                         │
│  13. Group Anagrams     │                         │  53. Clone Graph        │                         │
│  14. Spiral Matrix      │                         │  54. Course Schedule    │                         │
│  15. Rotate Image       │                         │  55. Course Schedule II │                         │
│  16. Set Matrix Zeroes  │                         │  56. Word Search        │                         │
│  17. Search Rotated     │                         │  57. Implement Trie     │                         │
│  18. Find First/Last    │                         │  58. Add/Search Word    │                         │
│  19. Merge Intervals    │                         │  59. BT Right Side      │                         │
│  20. Insert Interval    │                         │  60. Count Good Nodes   │                         │
│  21. Subarray Sum K     │                         │                         │                         │
│  22. Next Permutation   │                         │ HARD (5):               │                         │
│  23. Min Window Sub     │                         │  61. BT Max Path Sum    │                         │
│  24. Valid Anagram      │                         │  62. Serialize BT       │                         │
│                         │                         │  63. Word Search II     │                         │
│ HARD (6):               │                         │  64. Alien Dictionary   │                         │
│  25. Trapping Rain      │                         │  65. Word Ladder        │                         │
│  26. Median Two Arrays  │                         │                         │                         │
│  27. First Missing +    │                         │                         │                         │
│  28. Longest Consecutive│                         │                         │                         │
│  29. Sliding Window Max │                         │                         │                         │
│  30. Min Window Sub     │                         │                         │                         │
└─────────────────────────┴─────────────────────────┴─────────────────────────┴─────────────────────────┘

┌─────────────────────────┬─────────────────────────┬─────────────────────────┐
│   HASH TABLE (8)        │   HEAP/PQ (5)           │   DYNAMIC PROG (12)     │
├─────────────────────────┼─────────────────────────┼─────────────────────────┤
│                         │                         │                         │
│ EASY (3):               │ EASY (1):               │ EASY (3):               │
│  74. Two Sum            │  82. Kth Largest Stream │  87. Climbing Stairs    │
│  75. Valid Anagram      │                         │  88. House Robber       │
│  76. Contains Duplicate │ MEDIUM (3):             │  89. Maximum Subarray   │
│                         │  83. Kth Largest Array  │                         │
│ MEDIUM (5):             │  84. Top K Frequent     │ MEDIUM (7):             │
│  77. Group Anagrams     │  85. Find Median Stream │  90. Coin Change        │
│  78. Top K Frequent     │                         │  91. Longest Increasing │
│  79. Encode/Decode Str  │ HARD (1):               │  92. Longest Common Sub │
│  80. Longest Consecutive│  86. Merge K Lists      │  93. Word Break         │
│  81. LRU Cache          │                         │  94. Combination Sum IV │
│                         │                         │  95. House Robber II    │
│                         │                         │  96. Decode Ways        │
│                         │                         │  97. Unique Paths       │
│                         │                         │  98. Jump Game          │
│                         │                         │                         │
│                         │                         │ HARD (2):               │
│                         │                         │  99. Edit Distance      │
│                         │                         │  100. Regex Matching    │
└─────────────────────────┴─────────────────────────┴─────────────────────────┘
```

---

## COMPLETE PROBLEM LIST BY ALGORITHM/CONCEPT

```
┌──────────────────────────────┬──────────────────────────────┬──────────────────────────────┐
│   TWO POINTERS (15)          │   SLIDING WINDOW (8)         │   BINARY SEARCH (10)         │
├──────────────────────────────┼──────────────────────────────┼──────────────────────────────┤
│                              │                              │                              │
│ → Two Sum II (Sorted)        │ → Longest Substring (No Rep) │ → Binary Search (Basic)      │
│ → 3Sum                       │ → Minimum Window Substring   │ → Search Rotated Array       │
│ → 3Sum Closest               │ → Longest Repeating Char     │ → Find Min Rotated Array     │
│ → Container With Most Water  │ → Permutation in String      │ → Search 2D Matrix           │
│ → Remove Duplicates (Sorted) │ → Sliding Window Maximum     │ → Kth Smallest Sorted Matrix │
│ → Valid Palindrome           │ → Maximum Average Subarray   │ → Median of Two Arrays       │
│ → Reverse String             │ → Minimum Size Subarray Sum  │ → Find Peak Element          │
│ → Merge Sorted Array         │ → Find All Anagrams          │ → Search Insert Position     │
│ → Move Zeroes                │                              │ → Time Based Key-Value       │
│ → Sort Colors                │                              │ → Find First/Last Position   │
│ → Remove Nth Node (LL)       │                              │                              │
│ → Linked List Cycle          │                              │                              │
│ → Palindrome Linked List     │                              │                              │
│ → Trapping Rain Water        │                              │                              │
│ → Minimum Size Subarray Sum  │                              │                              │
└──────────────────────────────┴──────────────────────────────┴──────────────────────────────┘

┌───────────────────────────────────────────────────────────┬──────────────────────────────┐
│              DFS / BFS (20)                               │   DYNAMIC PROGRAMMING (18)   │
├───────────────────────────────────────────────────────────┼──────────────────────────────┤
│                                                           │                              │
│ TREE PROBLEMS (7):                                        │ 1D DP (10):                  │
│  → Binary Tree Level Order Traversal                      │  → Climbing Stairs           │
│  → Binary Tree Inorder Traversal                          │  → House Robber              │
│  → Binary Tree Zigzag Level Order                         │  → House Robber II           │
│  → Binary Tree Right Side View                            │  → Decode Ways               │
│  → Maximum Depth of Binary Tree                           │  → Coin Change               │
│  → Same Tree                                              │  → Maximum Product Subarray  │
│  → Symmetric Tree                                         │  → Word Break                │
│                                                           │  → Longest Increasing Subseq │
│ GRAPH PROBLEMS (13):                                      │  → Jump Game                 │
│  → Number of Islands                                      │  → Combination Sum IV        │
│  → Clone Graph                                            │                              │
│  → Max Area of Island                                     │ 2D DP (5):                   │
│  → Pacific Atlantic Water Flow                            │  → Longest Common Subsequence│
│  → Surrounded Regions                                     │  → Edit Distance             │
│  → Course Schedule (Topological)                          │  → Unique Paths              │
│  → Course Schedule II                                     │  → Longest Palindrome String │
│  → Word Search (Backtrack+DFS)                            │  → Palindromic Substrings    │
│  → Word Ladder (BFS Shortest)                             │                              │
│  → All Paths Source to Target                             │ ADVANCED DP (3):             │
│  → Rotting Oranges                                        │  → Partition Equal Subset    │
│  → Walls and Gates                                        │  → Target Sum                │
│  → Graph Valid Tree                                       │  → Best Time Buy/Sell Stock  │
│  → Shortest Path Binary Matrix                            │                              │
│  → Open the Lock                                          │                              │
│  → Minimum Height Trees                                   │                              │
│  → Flood Fill                                             │                              │
│  → Keys and Rooms                                         │                              │
└───────────────────────────────────────────────────────────┴──────────────────────────────┘

┌──────────────────────────────┬──────────────────────────────┬──────────────────────────────┐
│   BACKTRACKING (10)          │   GREEDY (8)                 │   DIVIDE & CONQUER (5)       │
├──────────────────────────────┼──────────────────────────────┼──────────────────────────────┤
│                              │                              │                              │
│ → Permutations               │ → Jump Game                  │ → Merge Sort                 │
│ → Subsets                    │ → Jump Game II               │ → Quick Sort                 │
│ → Combination Sum            │ → Gas Station                │ → Median of Two Arrays       │
│ → Letter Combo Phone Number  │ → Hand of Straights          │ → Kth Largest Element        │
│ → Generate Parentheses       │ → Merge Triplets Target      │ → Maximum Subarray           │
│ → Word Search                │ → Partition Labels           │                              │
│ → N-Queens                   │ → Valid Parenthesis String   │                              │
│ → Palindrome Partitioning    │ → Meeting Rooms II           │                              │
│ → Sudoku Solver              │                              │                              │
│ → Restore IP Addresses       │                              │                              │
└──────────────────────────────┴──────────────────────────────┴──────────────────────────────┘
```

---

## DIFFICULTY DISTRIBUTION

```
TOTAL: 100 PROBLEMS

EASY (25 Problems - 25%)
═════════════════════════════════════════════════════════════════
██████████████████████████████████████████████████

MEDIUM (55 Problems - 55%)
═════════════════════════════════════════════════════════════════
██████████████████████████████████████████████████████████████████████████████████████████████████████████████

HARD (20 Problems - 20%)
═════════════════════════════════════════════════════════════════
████████████████████████████████████████
```

---

## STUDY ROADMAP (16 Weeks)

```
START HERE
    |
    ↓
WEEK 1-2: FOUNDATION
    |
    ├───→ Arrays & Strings (10 problems)
    |       • Two Sum, Contains Duplicate, Valid Palindrome
    |       • Maximum Subarray, Merge Sorted Array
    |       • Product of Array Except Self
    |       • Longest Substring Without Repeating
    |
    └───→ Hash Tables (5 problems)
            • Two Sum, Valid Anagram, Group Anagrams
            • Top K Frequent Elements
    ↓

WEEK 3: SEARCH & WINDOW
    |
    ├───→ Two Pointers (8 problems)
    |       • 3Sum, Container With Most Water
    |       • Valid Palindrome, Trapping Rain Water
    |
    └───→ Sliding Window (6 problems)
            • Longest Substring, Minimum Window
            • Sliding Window Maximum
    ↓

WEEK 4: LINEAR STRUCTURES
    |
    ├───→ Linked Lists (10 problems)
    |       • Reverse Linked List, Merge Two Lists
    |       • Detect Cycle, Remove Nth Node
    |       • Merge K Sorted Lists
    |
    └───→ Stacks & Queues (8 problems)
            • Valid Parentheses, Min Stack
            • Daily Temperatures, Largest Rectangle
    ↓

WEEK 5-6: TREES
    |
    ├───→ Binary Trees Basics (8 problems)
    |       • Max Depth, Same Tree, Invert Tree
    |       • Level Order Traversal, Right Side View
    |
    ├───→ Binary Search Trees (5 problems)
    |       • Validate BST, Kth Smallest in BST
    |       • Lowest Common Ancestor
    |
    └───→ Advanced Trees (5 problems)
            • Serialize/Deserialize, Maximum Path Sum
            • Implement Trie, Word Search II
    ↓

WEEK 7-8: GRAPHS
    |
    ├───→ Graph Traversal (8 problems)
    |       • Number of Islands, Clone Graph
    |       • Max Area of Island, Surrounded Regions
    |
    ├───→ Topological Sort (3 problems)
    |       • Course Schedule, Course Schedule II
    |
    └───→ Advanced Graph (4 problems)
            • Word Ladder, Shortest Path in Matrix
            • Graph Valid Tree
    ↓

WEEK 9-11: DYNAMIC PROGRAMMING
    |
    ├───→ 1D DP (10 problems)
    |       • Climbing Stairs, House Robber
    |       • Coin Change, Decode Ways
    |       • Longest Increasing Subsequence
    |
    ├───→ 2D DP (5 problems)
    |       • Unique Paths, Longest Common Subsequence
    |       • Edit Distance
    |
    └───→ Advanced DP (3 problems)
            • Partition Equal Subset Sum, Target Sum
    ↓

WEEK 12-13: BACKTRACKING & ADVANCED
    |
    ├───→ Backtracking (10 problems)
    |       • Permutations, Subsets, Combination Sum
    |       • N-Queens, Sudoku Solver
    |
    ├───→ Greedy (8 problems)
    |       • Jump Game, Gas Station, Meeting Rooms
    |
    └───→ Heap (5 problems)
            • Kth Largest, Merge K Lists
            • Find Median from Data Stream
    ↓

WEEK 14-16: PRACTICE & REVIEW
    |
    ├───→ Week 14: Mixed Easy/Medium (15 problems)
    ├───→ Week 15: Hard Problems (10 problems)
    └───→ Week 16: Mock Interviews & Company Questions

    ↓
INTERVIEW READY! 🎯
```

---

## PATTERN RECOGNITION FLOWCHART

```
                    PROBLEM ANALYSIS
                           |
    ┌──────────────────────┼──────────────────────┐
    |                      |                      |
    ↓                      ↓                      ↓
ARRAY/STRING          LINKED LIST           TREE/GRAPH
    |                      |                      |
    ↓                      ↓                      ↓
Is Sorted?            Fast/Slow Ptr?         Traversal?
    |                      |                      |
   YES                    YES                    YES
    |                      |                      |
    ↓                      ↓                      ↓
Binary Search         Find Cycle            DFS/BFS
Two Pointers          Find Middle               |
    |                 Detect Loop               ↓
   NO                      |                 Shortest Path?
    |                     NO                     |
    ↓                      |                    YES
Subarray/              Reverse?                  |
Substring?                 |                     ↓
    |                     YES                   BFS
   YES                     |                     |
    |                      ↓                    NO
    ↓                 Reverse                    |
Sliding Window         Technique                 ↓
Prefix Sum                                   All Paths?
    |                                             |
   NO                                            YES
    |                                             |
    ↓                                             ↓
Hash Table                                       DFS
                                            Backtracking


                OPTIMIZATION PROBLEMS
                         |
    ┌────────────────────┼────────────────────┐
    |                    |                    |
    ↓                    ↓                    ↓
Multiple Choices?   Generate All?      Intervals?
    |                    |                    |
   YES                  YES                  YES
    |                    |                    |
    ↓                    ↓                    ↓
Overlapping         Backtracking          Greedy
Subproblems?             |                Sorting
    |                   NO                    |
   YES                   |                   NO
    |                    ↓                    |
    ↓               Combinations              ↓
Dynamic                                   Scheduling
Programming


                K-TH ELEMENT PROBLEMS
                         |
    ┌────────────────────┼────────────────────┐
    |                    |                    |
    ↓                    ↓                    ↓
Find Kth          Top K Elements      Median/Stream
Largest?               |                     |
    |                  ↓                     ↓
    ↓              Heap/PQ              Two Heaps
Quick Select       (Min/Max)           (Min + Max)
Heap
```

---

## PATTERN → PROBLEM MAPPING

```
PATTERN                              PROBLEMS
═══════════════════════════════════════════════════════════════════

TWO POINTERS                    →    3Sum
  (Sorted/Pairs)                →    Container With Most Water
                                →    Trapping Rain Water
                                →    Valid Palindrome
                                ↓

SLIDING WINDOW                  →    Longest Substring (No Repeat)
  (Subarray/Substring)          →    Minimum Window Substring
                                →    Max Sliding Window
                                →    Find All Anagrams
                                ↓

BINARY SEARCH                   →    Search Rotated Sorted Array
  (Sorted/Find)                 →    Median of Two Sorted Arrays
                                →    Find First/Last Position
                                →    Kth Smallest in Matrix
                                ↓

HASH TABLE                      →    Two Sum
  (Fast Lookup)                 →    Group Anagrams
                                →    Longest Consecutive Sequence
                                →    LRU Cache
                                ↓

DFS                             →    Number of Islands
  (All Paths/Components)        →    Word Search
                                →    Clone Graph
                                →    Course Schedule
                                ↓

BFS                             →    Binary Tree Level Order
  (Shortest/Level)              →    Word Ladder
                                →    Rotting Oranges
                                →    Shortest Path in Matrix
                                ↓

DYNAMIC PROGRAMMING             →    Climbing Stairs
  (Count Ways/Min-Max)          →    Coin Change
                                →    Longest Increasing Subsequence
                                →    Edit Distance
                                ↓

BACKTRACKING                    →    Permutations
  (Generate All)                →    Subsets
                                →    N-Queens
                                →    Combination Sum
                                ↓

GREEDY                          →    Jump Game
  (Local Optimal)               →    Gas Station
                                →    Meeting Rooms II
                                →    Partition Labels
                                ↓

HEAP / PRIORITY QUEUE           →    Kth Largest Element
  (K-th Element)                →    Merge K Sorted Lists
                                →    Top K Frequent
                                →    Find Median from Stream
                                ↓
```

---

## QUICK PROBLEM LOOKUP TABLE

```
PROBLEM TYPE                    GO TO PATTERN
═══════════════════════════════════════════════════════════════════

Sorted Array + Target      →    Binary Search / Two Pointers

Subarray/Substring         →    Sliding Window / Prefix Sum

Pairs/Triplets/Sum         →    Two Pointers / Hash Table

Palindrome                 →    Two Pointers / DP

Tree Traversal             →    DFS (Recursive) / BFS (Iterative)

Graph Shortest Path        →    BFS / Dijkstra

Graph All Paths            →    DFS / Backtracking

Connected Components       →    DFS / BFS / Union Find

Cycle Detection            →    DFS / Slow-Fast Pointer

Count Ways                 →    Dynamic Programming

Min/Max Optimization       →    DP / Greedy

Generate All Combinations  →    Backtracking

Interval Scheduling        →    Greedy + Sorting

K-th Largest/Smallest      →    Heap / Quick Select

Top K Elements             →    Heap / Bucket Sort

Median/Running Stats       →    Two Heaps (Min + Max)

LRU/LFU Cache              →    Hash Table + Doubly Linked List

Prefix/Suffix              →    Trie / Hash Table

Topological Ordering       →    Kahn's Algorithm / DFS
```

---

## COMPLEXITY CHEAT SHEET

```
ALGORITHM                TIME           SPACE        WHEN TO USE
═══════════════════════════════════════════════════════════════════════

Two Pointers            O(n)           O(1)         Sorted, pairs, palindrome

Sliding Window          O(n)           O(k)         Subarray/substring

Binary Search           O(log n)       O(1)         Sorted array, search

Hash Table              O(n)           O(n)         Fast lookup, duplicates

DFS                     O(V+E)         O(h)         All paths, components

BFS                     O(V+E)         O(w)         Shortest path, levels

Dynamic Programming     O(n²) avg      O(n) avg     Overlapping subproblems

Backtracking            O(2ⁿ) avg      O(n)         Generate all solutions

Greedy                  O(n log n)     O(1)         Optimal local choice

Heap                    O(n log k)     O(k)         K-th element, top K

Quick Select            O(n) avg       O(1)         K-th element (one-time)

Trie                    O(m)           O(n*m)       Prefix search, autocomplete

Union Find              O(α(n))        O(n)         Connected components

Topological Sort        O(V+E)         O(V)         DAG ordering
```

---

## SUCCESS TIPS

```
                    INTERVIEW PREPARATION
                            |
    ┌───────────────────────┼───────────────────────┐
    |                       |                       |
    ↓                       ↓                       ↓
UNDERSTAND            PRACTICE              OPTIMIZE
    |                       |                       |
    ↓                       ↓                       ↓
Pattern                2-3 Daily           Brute → Better
Recognition            Problems            → Optimal
    |                       |                       |
Don't                  Time               Think Aloud
Memorize              Yourself            Explain Logic
    |                       |                       |
Focus on              Review              Test Edge
Why not What          Mistakes            Cases
    ↓                       ↓                       ↓


            COMMON MISTAKES TO AVOID
                    |
    ┌───────────────┼───────────────┐
    |               |               |
    ↓               ↓               ↓
Not Testing     Jumping to      Ignoring
Edge Cases      Code Too        Time/Space
    |           Fast            Complexity
    |               |               |
    ↓               ↓               ↓
• Empty         • Think         • Always
• Single        • Plan          • Analyze
• Duplicates    • Then Code     • First
• Large N       • Verify        • Optimize
    ↓               ↓               ↓
```

---

## RESOURCES

```
LEARNING PLATFORMS
    |
    ├───→ LeetCode Explore Cards (Guided Learning)
    ├───→ NeetCode 150 (Video Solutions)
    ├───→ Blind 75 (Essential Problems)
    └───→ Grind 75 (Customized Study Plan)

PRACTICE STRATEGIES
    |
    ├───→ Week 1-8:   Focus on Patterns (Learn)
    ├───→ Week 9-12:  Mixed Practice (Apply)
    └───→ Week 13-16: Mock Interviews (Master)

INTERVIEW TIPS
    |
    ├───→ Clarify Requirements First
    ├───→ Discuss Approach Before Coding
    ├───→ Write Clean, Readable Code
    ├───→ Test with Examples
    └───→ Discuss Trade-offs & Optimizations
```

---

## FINAL STATS

```
╔═══════════════════════════════════════════════════════════════╗
║                  TOP 100 LEETCODE PROBLEMS                    ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  TOTAL PROBLEMS:              100                             ║
║                                                               ║
║  BY DIFFICULTY:                                               ║
║    • Easy:                    25  (25%)                       ║
║    • Medium:                  55  (55%)                       ║
║    • Hard:                    20  (20%)                       ║
║                                                               ║
║  BY DATA STRUCTURE:                                           ║
║    • Array/String             30  (30%)                       ║
║    • Tree/Graph               25  (25%)                       ║
║    • Dynamic Programming      12  (12%)                       ║
║    • Linked List              10  (10%)                       ║
║    • Stack/Queue               8  (8%)                        ║
║    • Hash Table                8  (8%)                        ║
║    • Heap/Priority Queue       5  (5%)                        ║
║    • Other                     2  (2%)                        ║
║                                                               ║
║  BY ALGORITHM:                                                ║
║    • DFS/BFS                  20  (20%)                       ║
║    • Dynamic Programming      18  (18%)                       ║
║    • Two Pointers             15  (15%)                       ║
║    • Backtracking             10  (10%)                       ║
║    • Binary Search            10  (10%)                       ║
║    • Sliding Window            8  (8%)                        ║
║    • Greedy                    8  (8%)                        ║
║    • Divide & Conquer          5  (5%)                        ║
║    • Other                     6  (6%)                        ║
║                                                               ║
║  ESTIMATED STUDY TIME:                                        ║
║    • Full Coverage:           16 weeks (2-3 problems/day)     ║
║    • Intensive:               8 weeks (4-5 problems/day)      ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

**END OF VISUAL GUIDE**
