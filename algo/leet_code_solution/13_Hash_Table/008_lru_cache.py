"""
LeetCode Problem #146: LRU Cache

Difficulty: Medium
Topics: Hash Table, Linked List, Design, Doubly-Linked List
Companies: Amazon, Facebook, Google, Microsoft, Apple, Uber, Bloomberg, LinkedIn

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
│ 4    │ 💡 SOLUTION 1: HashMap + DLL ⭐      │ • WHY choose? (Pros/Cons)     │
│      │    (OPTIMAL - O(1))                  │ • WHEN to use?                │
│      │                                      │ • Step-by-step walkthrough    │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 5    │ 💡 SOLUTION 2: OrderedDict           │ • WHY choose? (Pros/Cons)     │
│      │    (Python Built-in)                 │ • WHEN to use?                │
│      │                                      │ • Comparison with Solution 1  │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 6    │ 💡 SOLUTION 3: Array (Not Optimal)   │ • WHY NOT recommended?        │
│      │    (Educational)                     │ • What's wrong?               │
│      │                                      │ • Why O(N) operations fail    │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 7    │ 💻 IMPLEMENTATION                    │ • Clean, commented code       │
│      │                                      │ • All three solutions         │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 8    │ 🧪 TEST CASES                        │ • Comprehensive tests         │
│      │                                      │ • Edge cases covered          │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 9    │ 🎓 LEARNING SUMMARY                  │ • Key takeaways               │
│      │                                      │ • Memory tricks               │
│      │                                      │ • Common mistakes             │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 10   │ 🔗 RELATED PROBLEMS                  │ • Similar problems            │
│      │                                      │ • Pattern recognition         │
└──────┴──────────────────────────────────────┴───────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                           🎯 MEMORY CHEAT SHEET                             │
├──────────────────┬──────────────────────────────────────────────────────────┤
│ ANALOGY          │ "Browser Tabs" - Close least used tab when limit hit!  │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ PATTERN          │ "HashMap + Doubly Linked List" - Best of both worlds!   │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ KEY TRICK        │ HashMap for O(1) access, DLL for O(1) reordering!       │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ DEFAULT SOLUTION │ HashMap + DLL (O(1) for all operations!)                │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ TIME COMPLEXITY  │ O(1) - Constant time for get() and put()                │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ SPACE COMPLEXITY │ O(capacity) - Store at most 'capacity' items            │
└──────────────────┴──────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                        ⚡ QUICK DECISION TABLE                              │
├────────────────────────────────┬────────────────────────────────────────────┤
│ SITUATION                      │ WHICH SOLUTION TO USE?                    │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Normal interview               │ ✅ Solution 1 (HashMap + DLL)             │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Want optimal O(1) solution     │ ✅ Solution 1 (Industry standard!)        │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Python-specific interview      │ ⚡ Solution 2 (OrderedDict - cleaner)     │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Learning data structures       │ 🎓 Solution 1 (teaches DLL mastery)      │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Real production system         │ ✅ Solution 1 (most efficient!)           │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Want to show optimization      │ 🎯 Explain Sol 3, optimize to Sol 1     │
└────────────────────────────────┴────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                     📊 SOLUTION COMPARISON TABLE                            │
├──────────────────┬──────────────┬──────────────┬──────────────┬─────────────┤
│ CRITERIA         │ HASHMAP+DLL  │ ORDEREDDICT  │ ARRAY        │ WINNER      │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Time: get()      │ ⭐⭐⭐⭐⭐   │ ⭐⭐⭐⭐⭐   │ ⭐⭐         │ HashMap/OD  │
│                  │ O(1)         │ O(1)         │ O(N)         │             │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Time: put()      │ ⭐⭐⭐⭐⭐   │ ⭐⭐⭐⭐⭐   │ ⭐⭐         │ HashMap/OD  │
│                  │ O(1)         │ O(1)         │ O(N)         │             │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Space Complexity │ ⭐⭐⭐⭐     │ ⭐⭐⭐⭐     │ ⭐⭐⭐⭐⭐   │ Array       │
│                  │ O(capacity)  │ O(capacity)  │ O(capacity)  │             │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Code Complexity  │ ⭐⭐⭐       │ ⭐⭐⭐⭐⭐   │ ⭐⭐⭐⭐     │ OrderedDict │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Interview Speed  │ ⭐⭐⭐⭐     │ ⭐⭐⭐⭐⭐   │ ⭐⭐⭐⭐     │ OrderedDict │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Industry Use     │ ⭐⭐⭐⭐⭐   │ ⭐⭐⭐       │ ⭐           │ HashMap+DLL │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Overall Best     │ ✅ YES       │ Good (Py)    │ Avoid        │ HashMap+DLL │
└──────────────────┴──────────────┴──────────────┴──────────────┴─────────────┘

⏱️  TIME TO MASTER: 30-35 minutes
🎯 DIFFICULTY: Medium (but feels Hard without the pattern!)
💡 TIP: "HashMap finds it, Doubly Linked List orders it!"
🔥 POPULAR: Asked in 95% of system design interviews!

================================================================================
                           🎯 PROBLEM UNDERSTANDING
================================================================================

WHAT IS THE PROBLEM?
--------------------
Design a cache that automatically evicts the LEAST RECENTLY USED item when full.
Both get() and put() operations must be O(1) time!

REAL WORLD ANALOGY:
------------------
Think of it like BROWSER TABS with limited memory:
- You have 3 tab slots available (capacity = 3)
- Opening tabs: Tab1, Tab2, Tab3 (all slots full!)
- Open Tab4 → Close LEAST RECENTLY USED tab (maybe Tab1)
- Click on Tab2 (use it) → Now Tab2 is most recently used
- Open Tab5 → Close least used (maybe Tab3)

Another analogy - MUSIC PLAYLIST CACHE:
- Phone can cache 5 songs (capacity = 5)
- Play songs: [Song A, Song B, Song C, Song D, Song E] (full!)
- Play Song F → Remove least recently played (Song A)
- Play Song B again → Song B becomes most recently used
- Play Song G → Remove least used (maybe Song C)

THE KEY INSIGHT:
---------------
Need TWO data structures working together:
1. HashMap: For O(1) access to values
2. Doubly Linked List: For O(1) reordering (most recent ↔ least recent)

❌ Wrong thinking: "Use HashMap alone" → Can't track order efficiently
❌ Wrong thinking: "Use List alone" → Can't find items in O(1)
✅ Right thinking: "Combine HashMap + Doubly Linked List!"

================================================================================
                            📝 FORMAL PROBLEM
================================================================================

Design a data structure that follows the constraints of a Least Recently Used
(LRU) cache.

Implement the LRUCache class:
- LRUCache(int capacity): Initialize the LRU cache with positive size capacity
- int get(int key): Return the value if key exists, otherwise return -1
  * The get() operation counts as "using" the key (moves to most recent)
- void put(int key, int value): Update value if key exists, or add new pair
  * If adding would exceed capacity, evict the least recently used key

Both get() and put() must run in O(1) average time complexity.

Example 1:
----------
Input:
["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]
[[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]

Output:
[null, null, null, 1, null, -1, null, -1, 3, 4]

Explanation:
LRUCache cache = new LRUCache(2);  // capacity = 2
cache.put(1, 1);  // cache: {1=1}
cache.put(2, 2);  // cache: {1=1, 2=2}
cache.get(1);     // returns 1, cache: {2=2, 1=1} (1 is now MRU)
cache.put(3, 3);  // evicts key 2, cache: {1=1, 3=3}
cache.get(2);     // returns -1 (not found)
cache.put(4, 4);  // evicts key 1, cache: {3=3, 4=4}
cache.get(1);     // returns -1 (not found)
cache.get(3);     // returns 3
cache.get(4);     // returns 4

Constraints:
------------
* 1 <= capacity <= 3000
* 0 <= key <= 10^4
* 0 <= value <= 10^5
* At most 2 * 10^5 calls will be made to get and put
* Both operations must be O(1) time

================================================================================
                         🧠 KEY INSIGHTS TO REMEMBER
================================================================================

THE MAIN CHALLENGE:
------------------
❌ HashMap alone: Can find in O(1), but can't track order efficiently
❌ Array/List alone: Can't find items in O(1)
❌ Singly Linked List: Can't remove from middle in O(1)
✅ HashMap + Doubly Linked List: Perfect combination!

THE MAGIC TRICK: "DUMMY HEAD AND TAIL"
---------------------------------------
Key observation: Doubly Linked List with dummy nodes!

Structure:
  head (dummy) ↔ [MRU] ↔ [item] ↔ ... ↔ [item] ↔ [LRU] ↔ tail (dummy)

  - head.next = Most Recently Used
  - tail.prev = Least Recently Used
  - Dummy nodes eliminate edge cases!

THE BREAKTHROUGH INSIGHT:
------------------------
┌─────────────────────────────────────────────────────────────┐
│  HashMap: key → Node (O(1) access)                          │
│  Doubly Linked List: Order from MRU to LRU (O(1) reorder)   │
│  → Combined: O(1) for all operations!                       │
└─────────────────────────────────────────────────────────────┘

WHY DOUBLY LINKED LIST?
-----------------------
- Singly linked: Can't remove from middle efficiently
- Doubly linked: Can remove ANY node in O(1)
  * node.prev.next = node.next
  * node.next.prev = node.prev
  * Done! Removed in O(1)!

OPERATIONS:
-----------
1. get(key):
   - If key exists: move to head (MRU position), return value
   - If not: return -1

2. put(key, value):
   - If key exists: update value, move to head
   - If new key:
     * Add to head (MRU position)
     * If over capacity: remove tail.prev (LRU item)

================================================================================
                          💡 SOLUTION APPROACHES
================================================================================
"""

from typing import Optional

# ============================================================================
#          APPROACH 1: HASHMAP + DOUBLY LINKED LIST (OPTIMAL)
# ============================================================================

class Node:
    """Node for doubly linked list."""
    def __init__(self, key: int = 0, value: int = 0):
        self.key = key
        self.value = value
        self.prev: Optional[Node] = None
        self.next: Optional[Node] = None


class LRUCache:
    """
    🎯 APPROACH 1: HashMap + Doubly Linked List (BEST SOLUTION!)

    TIME COMPLEXITY: O(1) - Both get() and put()
    SPACE COMPLEXITY: O(capacity) - Store at most capacity items

    🧠 MEMORIZATION TRICK: "HashMap Finds, DLL Orders"
    --------------------------------------------------
    Think: Like a library with an index card system!
    - HashMap (card catalog): Find book location instantly
    - Doubly Linked List (shelf): Books ordered by last checkout
    - Most recent checkouts at front
    - Least recent at back → remove first when shelf full

    📝 DATA STRUCTURE:
    ------------------
    HashMap: {key → Node in linked list}
    Doubly Linked List:
      head (dummy) ↔ [Node] ↔ [Node] ↔ ... ↔ [Node] ↔ tail (dummy)
                      ↑MRU                        ↑LRU

    📝 OPERATIONS:
    --------------
    get(key):
      1. If key not in HashMap → return -1
      2. Get node from HashMap
      3. Move node to head (mark as MRU)
      4. Return node.value
      Time: O(1)

    put(key, value):
      Case 1: Key exists
        1. Get node from HashMap
        2. Update node.value
        3. Move to head (mark as MRU)

      Case 2: New key
        1. Create new node
        2. Add to HashMap
        3. Add to head of DLL
        4. If size > capacity:
           - Remove tail.prev (LRU node)
           - Delete from HashMap
      Time: O(1)

    🎨 VISUAL EXAMPLE:
    -----------------
    capacity = 2

    Initial state:
      head ↔ tail
      HashMap: {}

    put(1, 1):
      head ↔ [1,1] ↔ tail
      HashMap: {1 → Node(1,1)}

    put(2, 2):
      head ↔ [2,2] ↔ [1,1] ↔ tail
             ↑MRU          ↑LRU
      HashMap: {1 → Node(1,1), 2 → Node(2,2)}

    get(1):  (returns 1, moves to head)
      head ↔ [1,1] ↔ [2,2] ↔ tail
             ↑MRU          ↑LRU

    put(3, 3):  (capacity full, evict LRU which is 2)
      Remove [2,2] from list and HashMap
      head ↔ [3,3] ↔ [1,1] ↔ tail
             ↑MRU          ↑LRU
      HashMap: {1 → Node(1,1), 3 → Node(3,3)}

    WHY THIS IS O(1):
    -----------------
    ✅ HashMap lookup: O(1)
    ✅ Remove from DLL: O(1) (update pointers)
    ✅ Add to head: O(1) (update pointers)
    ✅ Remove from tail: O(1) (tail.prev)

    All pointer operations are constant time!
    """

    def __init__(self, capacity: int):
        """Initialize LRU cache with given capacity."""
        self.capacity = capacity
        self.cache = {}  # key → Node

        # Dummy head and tail to eliminate edge cases
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node) -> None:
        """
        Remove node from doubly linked list.

        Before:  A ↔ node ↔ B
        After:   A ↔ B

        Time: O(1)
        """
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add_to_head(self, node: Node) -> None:
        """
        Add node right after head (most recent position).

        Before:  head ↔ A ↔ ...
        After:   head ↔ node ↔ A ↔ ...

        Time: O(1)
        """
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _move_to_head(self, node: Node) -> None:
        """
        Move existing node to head (mark as most recently used).

        Time: O(1) - Just remove and add
        """
        self._remove(node)
        self._add_to_head(node)

    def _remove_tail(self) -> Node:
        """
        Remove and return least recently used node (before tail).

        Before:  ... ↔ LRU ↔ tail
        After:   ... ↔ tail
        Return:  LRU node

        Time: O(1)
        """
        lru_node = self.tail.prev
        self._remove(lru_node)
        return lru_node

    def get(self, key: int) -> int:
        """
        Get value from cache.
        If exists, move to head (mark as recently used).

        Time: O(1)
        """
        if key not in self.cache:
            return -1

        node = self.cache[key]
        self._move_to_head(node)  # Mark as MRU
        return node.value

    def put(self, key: int, value: int) -> None:
        """
        Put key-value pair in cache.
        If key exists: update value and move to head.
        If new key: add to head and evict LRU if needed.

        Time: O(1)
        """
        if key in self.cache:
            # Key exists: update value and move to head
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            # New key: create node and add to head
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_to_head(new_node)

            # Check capacity and evict if needed
            if len(self.cache) > self.capacity:
                lru_node = self._remove_tail()
                del self.cache[lru_node.key]


# ============================================================================
#              APPROACH 2: ORDEREDDICT (PYTHON BUILT-IN)
# ============================================================================

from collections import OrderedDict

class LRUCache_OrderedDict:
    """
    🎯 APPROACH 2: Using Python's OrderedDict (SIMPLER!)

    TIME COMPLEXITY: O(1) - Both get() and put()
    SPACE COMPLEXITY: O(capacity)

    🧠 MEMORIZATION TRICK: "OrderedDict Remembers Insertion Order"
    ---------------------------------------------------------------
    Think: Python's OrderedDict is like a smart dictionary!
    - Maintains insertion order
    - move_to_end(key) moves item to end (most recent)
    - popitem(last=False) removes oldest item
    - Perfect for LRU cache!

    📝 OPERATIONS:
    --------------
    get(key):
      1. If key not in cache → return -1
      2. Move to end (mark as MRU)
      3. Return value

    put(key, value):
      1. If key exists: move to end
      2. Set cache[key] = value
      3. If size > capacity: popitem(last=False) to remove oldest

    🎨 VISUAL EXAMPLE:
    -----------------
    capacity = 2

    put(1, 1):  cache = OrderedDict([(1, 1)])
    put(2, 2):  cache = OrderedDict([(1, 1), (2, 2)])
    get(1):     cache = OrderedDict([(2, 2), (1, 1)])  ← 1 moved to end
    put(3, 3):  Remove oldest (2), add 3
                cache = OrderedDict([(1, 1), (3, 3)])

    ⚠️  WHY THIS WORKS:
    -------------------
    - OrderedDict maintains order internally using DLL!
    - move_to_end() is O(1)
    - popitem(last=False) is O(1)
    - Same underlying structure as our custom implementation!

    ✅ WHEN TO USE:
    ---------------
    - Python-specific interviews (if allowed)
    - Quick prototyping
    - When you want clean, readable code

    ❌ WHEN NOT TO USE:
    -------------------
    - Need to show data structure knowledge
    - Language-agnostic interview
    - Want to demonstrate pointer manipulation
    """

    def __init__(self, capacity: int):
        """Initialize LRU cache with given capacity."""
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        """
        Get value from cache.
        Move to end to mark as most recently used.

        Time: O(1)
        """
        if key not in self.cache:
            return -1

        # Move to end (most recent)
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        """
        Put key-value pair in cache.
        If exists: move to end. If new: add and evict if needed.

        Time: O(1)
        """
        if key in self.cache:
            # Move to end (mark as MRU)
            self.cache.move_to_end(key)

        self.cache[key] = value

        # Evict LRU if over capacity
        if len(self.cache) > self.capacity:
            # popitem(last=False) removes oldest (FIFO)
            self.cache.popitem(last=False)


# ============================================================================
#              APPROACH 3: ARRAY WITH TIMESTAMPS (NOT OPTIMAL)
# ============================================================================

import time

class LRUCache_Array:
    """
    🎯 APPROACH 3: Array with Timestamps (DON'T USE THIS!)

    TIME COMPLEXITY: O(N) - Need to scan array to find LRU
    SPACE COMPLEXITY: O(capacity)

    🧠 IDEA: Store items with timestamps
    -------------------------------------
    - Each item has: (key, value, timestamp)
    - get(): Update timestamp
    - put(): Find and remove item with oldest timestamp (O(N)!)

    ⚠️  PROBLEMS:
    ------------
    1. Finding LRU item requires scanning entire array → O(N)
    2. Removing from middle of array → O(N)
    3. Finding specific key → O(N) without additional HashMap
    4. Violates O(1) requirement!

    📝 ALGORITHM:
    ------------
    get(key):
      1. Scan array to find key → O(N)
      2. If found: update timestamp, return value
      3. If not: return -1

    put(key, value):
      1. Scan to find if key exists → O(N)
      2. If exists: update value and timestamp
      3. If new and array full:
         - Find item with minimum timestamp → O(N)
         - Remove it → O(N)
      4. Add new item

    ⚠️  WHY AVOID:
    -------------
    - All operations are O(N), not O(1)
    - Violates problem requirements
    - No advantage over HashMap + DLL
    - Only useful for understanding WHY we need better structures
    """

    def __init__(self, capacity: int):
        """Initialize cache with capacity."""
        self.capacity = capacity
        self.cache = []  # List of (key, value, timestamp)
        self.counter = 0  # Monotonic counter for order

    def get(self, key: int) -> int:
        """Get value - O(N) because we scan array."""
        for i, (k, v, _) in enumerate(self.cache):
            if k == key:
                # Update timestamp
                self.counter += 1
                self.cache[i] = (k, v, self.counter)
                return v
        return -1

    def put(self, key: int, value: int) -> None:
        """Put value - O(N) to find and potentially evict."""
        self.counter += 1

        # Check if key exists
        for i, (k, _, _) in enumerate(self.cache):
            if k == key:
                self.cache[i] = (k, value, self.counter)
                return

        # New key
        if len(self.cache) >= self.capacity:
            # Find LRU (minimum timestamp) - O(N)!
            lru_idx = min(range(len(self.cache)),
                         key=lambda i: self.cache[i][2])
            self.cache.pop(lru_idx)

        self.cache.append((key, value, self.counter))


# ============================================================================
#                    🎨 VISUAL WALKTHROUGH EXAMPLE
# ============================================================================

"""
Let's walk through the HashMap + DLL approach with:
capacity = 2
Operations: put(1,1), put(2,2), get(1), put(3,3), get(2), put(4,4)

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
                                            DETAILED STEP-BY-STEP VISUALIZATION
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ INITIAL STATE                                                                                                                   │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                                 │
│   Doubly Linked List Structure:                                                                                                │
│                                                                                                                                 │
│                    ┌────────────────┐                              ┌────────────────┐                                          │
│                    │      HEAD      │  ←─────────────────────────→ │      TAIL      │                                          │
│                    │  (dummy node)  │                              │  (dummy node)  │                                          │
│                    └────────────────┘                              └────────────────┘                                          │
│                                                                                                                                 │
│   HashMap (Key → Node):                                                                                                        │
│                    ┌──────────────────────────────────┐                                                                        │
│                    │         Empty {}                 │                                                                        │
│                    │     (No entries yet)             │                                                                        │
│                    └──────────────────────────────────┘                                                                        │
│                                                                                                                                 │
│   Cache Statistics:                                                                                                            │
│      • Current Size: 0 / 2                                                                                                     │
│      • Available Slots: 2                                                                                                      │
│                                                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ OPERATION 1: put(1, 1) — Adding first element to cache                                                                         │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                                 │
│   Steps Performed:                                                                                                             │
│      1. Create new Node(key=1, value=1)                                                                                        │
│      2. Add entry to HashMap: cache[1] = Node(1,1)                                                                             │
│      3. Insert node after HEAD (most recent position)                                                                          │
│      4. Update size: 0 → 1                                                                                                     │
│                                                                                                                                 │
│   BEFORE Operation:                                 AFTER Operation:                                                           │
│   ─────────────────                                 ───────────────                                                            │
│   HEAD ↔ TAIL                                       HEAD ↔ [Node 1:1] ↔ TAIL                                                  │
│   (empty cache)                                              ↑ MRU (Most Recently Used)                                        │
│                                                                                                                                 │
│                                                                                                                                 │
│   Detailed Doubly Linked List Structure (with pointers):                                                                       │
│                                                                                                                                 │
│       ┌──────────────┐        next         ┌──────────────────┐        next         ┌──────────────┐                          │
│       │     HEAD     │  ─────────────────→ │    Node 1:1      │  ─────────────────→ │     TAIL     │                          │
│       │  (dummy)     │                     │    key = 1       │                     │  (dummy)     │                          │
│       │              │  ←───────────────── │    value = 1     │  ←───────────────── │              │                          │
│       └──────────────┘        prev         └──────────────────┘        prev         └──────────────┘                          │
│                                                     ↑                                                                           │
│                                                     │                                                                           │
│   HashMap After Insertion:                          │                                                                           │
│   ─────────────────────────                         │                                                                           │
│       ┌────────────────────────────┐                │                                                                           │
│       │  Key 1  ───────────────────┴────────────────┘ (points to Node 1:1 in DLL)                                              │
│       └────────────────────────────┘                                                                                            │
│                                                                                                                                 │
│   Cache Statistics:                                                                                                            │
│      ✅ Size: 1 / 2                                                                                                            │
│      ✅ MRU (Most Recent): key=1                                                                                               │
│      ✅ LRU (Least Recent): key=1 (only element)                                                                               │
│                                                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ OPERATION 2: put(2, 2) — Cache now full!                                                                                       │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                                 │
│   Steps Performed:                                                                                                             │
│      1. Create new Node(key=2, value=2)                                                                                        │
│      2. Add entry to HashMap: cache[2] = Node(2,2)                                                                             │
│      3. Insert node after HEAD (new MRU, pushes previous node toward LRU)                                                      │
│      4. Update size: 1 → 2 (CACHE FULL!)                                                                                       │
│                                                                                                                                 │
│   Doubly Linked List Structure (with full pointers):                                                                           │
│                                                                                                                                 │
│       ┌──────────────┐       next        ┌──────────────────┐       next        ┌──────────────────┐       next        ┌──────────────┐
│       │     HEAD     │  ───────────────→ │    Node 2:2      │  ───────────────→ │    Node 1:1      │  ───────────────→ │     TAIL     │
│       │  (dummy)     │                   │    key = 2       │                   │    key = 1       │                   │  (dummy)     │
│       │              │  ←─────────────── │    value = 2     │  ←─────────────── │    value = 1     │  ←─────────────── │              │
│       └──────────────┘       prev        └──────────────────┘       prev        └──────────────────┘       prev        └──────────────┘
│                                                   ↑ MRU                                   ↑ LRU                                          │
│                                            (Most Recently Used)                    (Least Recently Used)                                 │
│                                                                                                                                 │
│   HashMap After Insertion:                                                                                                     │
│   ─────────────────────────                                                                                                    │
│       ┌────────────────────────────────────────────────────────────────────┐                                                   │
│       │  Key 2  ──────────┘ (points to Node 2:2 in DLL)                   │                                                   │
│       │  Key 1  ────────────────────────────────┘ (points to Node 1:1)    │                                                   │
│       └────────────────────────────────────────────────────────────────────┘                                                   │
│                                                                                                                                 │
│   Cache Statistics:                                                                                                            │
│      ✅ Size: 2 / 2 (CACHE FULL!)                                                                                              │
│      ✅ MRU (Most Recent): key=2 (just added)                                                                                  │
│      ✅ LRU (Least Recent): key=1 (oldest, will be evicted next if cache exceeds capacity)                                     │
│                                                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ OPERATION 3: get(1) → Returns 1 — Accessing existing key moves it to MRU position                                              │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                                 │
│   Steps Performed:                                                                                                             │
│      1. HashMap lookup: cache[1] exists ✅                                                                                     │
│      2. Get node reference from HashMap                                                                                        │
│      3. Move node to head (mark as MRU) via _move_to_head()                                                                    │
│         a. Remove from current position (disconnect pointers)                                                                  │
│         b. Insert after head (reconnect as MRU)                                                                                │
│      4. Return node.value = 1                                                                                                  │
│                                                                                                                                 │
│   BEFORE get(1):                                   AFTER get(1):                                                               │
│   ───────────────                                  ──────────────                                                              │
│   HEAD ↔ [2:2] ↔ [1:1] ↔ TAIL                     HEAD ↔ [1:1] ↔ [2:2] ↔ TAIL                                                │
│         ↑MRU           ↑LRU                               ↑MRU          ↑LRU                                                   │
│                                                                                                                                 │
│                                                                                                                                 │
│   Detailed Doubly Linked List Structure (AFTER get(1) - with full pointers):                                                  │
│                                                                                                                                 │
│       ┌──────────────┐       next        ┌──────────────────┐       next        ┌──────────────────┐       next        ┌──────────────┐
│       │     HEAD     │  ───────────────→ │    Node 1:1      │  ───────────────→ │    Node 2:2      │  ───────────────→ │     TAIL     │
│       │  (dummy)     │                   │    key = 1       │                   │    key = 2       │                   │  (dummy)     │
│       │              │  ←─────────────── │    value = 1     │  ←─────────────── │    value = 2     │  ←─────────────── │              │
│       └──────────────┘       prev        │    MOVED! ⭐      │       prev        └──────────────────┘       prev        └──────────────┘
│                                          └──────────────────┘                             ↑ LRU                                          │
│                                                   ↑ MRU (Most Recently Used)       (Least Recently Used - Next to evict)                  │
│                                             (Just accessed via get!)                                                                      │
│                                                                                                                                 │
│   HashMap After get(1):                                                                                                        │
│   ────────────────────                                                                                                         │
│       ┌────────────────────────────────────────────────────────────────────┐                                                   │
│       │  Key 2  ──────────────────────────────────┘ (points to Node 2:2)  │                                                   │
│       │  Key 1  ───────────────┘ (points to Node 1:1 - now at MRU!)       │                                                   │
│       └────────────────────────────────────────────────────────────────────┘                                                   │
│                                                                                                                                 │
│   Cache Statistics:                                                                                                            │
│      ✅ Size: 2 / 2 (FULL)                                                                                                     │
│      ✅ MRU (Most Recent): key=1 (just accessed!)                                                                              │
│      ✅ LRU (Least Recent): key=2 (will be evicted next if capacity exceeded)                                                  │
│                                                                                                                                 │
│   Return Value: 1 ✅                                                                                                            │
│                                                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ OPERATION 4: put(3, 3) → EVICTION REQUIRED! Cache full, must evict LRU to make room                                            │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                                 │
│   Steps Performed:                                                                                                             │
│      1. Create new Node(key=3, value=3)                                                                                        │
│      2. Add entry to HashMap: cache[3] = Node(3,3)                                                                             │
│      3. Insert node after HEAD (new MRU position)                                                                              │
│      4. Check size: len(cache) = 3 > capacity(2) → EVICTION REQUIRED!                                                          │
│      5. Remove tail.prev (the LRU node, which is key=2)                                                                        │
│      6. Delete key 2 from HashMap                                                                                              │
│                                                                                                                                 │
│   INTERMEDIATE STATE: After adding Node 3:3 but BEFORE eviction                                                                │
│   ─────────────────────────────────────────────────────────────                                                                │
│                                                                                                                                 │
│       HEAD ↔ [3:3] ↔ [1:1] ↔ [2:2] ↔ TAIL                                                                                     │
│             ↑NEW                    ↑LRU (will be evicted!)                                                                    │
│                                                                                                                                 │
│       Size: 3 items (exceeds capacity of 2!)                                                                                   │
│                                                                                                                                 │
│                                                                                                                                 │
│   FINAL STATE: After evicting Node 2:2 (LRU)                                                                                   │
│   ────────────────────────────────────────────                                                                                 │
│                                                                                                                                 │
│   Doubly Linked List Structure (with full pointers):                                                                           │
│                                                                                                                                 │
│       ┌──────────────┐       next        ┌──────────────────┐       next        ┌──────────────────┐       next        ┌──────────────┐
│       │     HEAD     │  ───────────────→ │    Node 3:3      │  ───────────────→ │    Node 1:1      │  ───────────────→ │     TAIL     │
│       │  (dummy)     │                   │    key = 3       │                   │    key = 1       │                   │  (dummy)     │
│       │              │  ←─────────────── │    value = 3     │  ←─────────────── │    value = 1     │  ←─────────────── │              │
│       └──────────────┘       prev        │    NEW! ⭐        │       prev        └──────────────────┘       prev        └──────────────┘
│                                          └──────────────────┘                             ↑ LRU                                          │
│                                                   ↑ MRU (Most Recently Used)       (Least Recently Used - Next to evict)                  │
│                                                (Just added!)                                                                              │
│                                                                                                                                 │
│                                                                                                                                 │
│   Node(2:2) EVICTED! ❌                                                                                                         │
│   ─────────────────────                                                                                                        │
│   • Removed from doubly linked list (tail.prev disconnected)                                                                   │
│   • Deleted from HashMap (key 2 no longer exists)                                                                              │
│   • Memory freed                                                                                                                │
│                                                                                                                                 │
│                                                                                                                                 │
│   HashMap After Eviction:                                                                                                      │
│   ───────────────────────                                                                                                      │
│       ┌────────────────────────────────────────────────────────────────────┐                                                   │
│       │  Key 3  ───────────────┘ (points to Node 3:3 in DLL - MRU)        │                                                   │
│       │  Key 1  ────────────────────────────────────┘ (points to Node 1:1) │                                                   │
│       │  Key 2  DELETED! ❌ (was evicted)                                  │                                                   │
│       └────────────────────────────────────────────────────────────────────┘                                                   │
│                                                                                                                                 │
│   Cache Statistics:                                                                                                            │
│      ✅ Size: 2 / 2 (back to capacity after eviction)                                                                          │
│      ✅ MRU (Most Recent): key=3 (just added)                                                                                  │
│      ✅ LRU (Least Recent): key=1 (will be evicted next if capacity exceeded)                                                  │
│                                                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ OPERATION 5: get(2) → Returns -1 (NOT FOUND) — Attempting to access evicted key                                                │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                                 │
│   Steps Performed:                                                                                                             │
│      1. HashMap lookup: cache[2] does NOT exist ❌                                                                             │
│      2. Return -1 (key not found)                                                                                              │
│                                                                                                                                 │
│   Doubly Linked List State (unchanged - no modifications):                                                                     │
│   ────────────────────────────────────────────────────────────                                                                 │
│                                                                                                                                 │
│       HEAD ↔ [3:3] ↔ [1:1] ↔ TAIL                                                                                             │
│             ↑MRU           ↑LRU                                                                                                │
│                                                                                                                                 │
│                                                                                                                                 │
│   HashMap State (unchanged):                                                                                                   │
│   ───────────────────────────                                                                                                  │
│       ┌────────────────────────────────────────────────────────────────────┐                                                   │
│       │  Key 3  ───→ Points to Node(3:3) in DLL                            │                                                   │
│       │  Key 1  ───→ Points to Node(1:1) in DLL                            │                                                   │
│       │  Key 2  NOT PRESENT! (was evicted in OPERATION 4) ❌               │                                                   │
│       └────────────────────────────────────────────────────────────────────┘                                                   │
│                                                                                                                                 │
│   Explanation:                                                                                                                 │
│   ──────────────                                                                                                               │
│   • Key 2 was evicted in the previous operation (OPERATION 4: put(3,3))                                                        │
│   • The HashMap no longer contains key 2                                                                                       │
│   • get() returns -1 to indicate key not found                                                                                 │
│   • Cache state remains unchanged (no side effects from failed lookup)                                                         │
│                                                                                                                                 │
│   Return Value: -1 ❌ (Key 2 was previously evicted and does not exist in cache)                                               │
│                                                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ OPERATION 6: put(4, 4) → EVICTION REQUIRED AGAIN! Adding new key when cache is full                                            │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                                 │
│   Steps Performed:                                                                                                             │
│      1. Create new Node(key=4, value=4)                                                                                        │
│      2. Add entry to HashMap: cache[4] = Node(4,4)                                                                             │
│      3. Insert node after HEAD (new MRU position)                                                                              │
│      4. Check size: len(cache) = 3 > capacity(2) → EVICTION REQUIRED!                                                          │
│      5. Remove tail.prev (the LRU node, which is key=1)                                                                        │
│      6. Delete key 1 from HashMap                                                                                              │
│                                                                                                                                 │
│   INTERMEDIATE STATE: After adding Node 4:4 but BEFORE eviction                                                                │
│   ─────────────────────────────────────────────────────────────                                                                │
│                                                                                                                                 │
│       HEAD ↔ [4:4] ↔ [3:3] ↔ [1:1] ↔ TAIL                                                                                     │
│             ↑NEW                    ↑LRU (will be evicted!)                                                                    │
│                                                                                                                                 │
│       Size: 3 items (exceeds capacity of 2!)                                                                                   │
│                                                                                                                                 │
│                                                                                                                                 │
│   FINAL STATE: After evicting Node 1:1 (LRU)                                                                                   │
│   ────────────────────────────────────────────                                                                                 │
│                                                                                                                                 │
│   Doubly Linked List Structure (with full pointers):                                                                           │
│                                                                                                                                 │
│       ┌──────────────┐       next        ┌──────────────────┐       next        ┌──────────────────┐       next        ┌──────────────┐
│       │     HEAD     │  ───────────────→ │    Node 4:4      │  ───────────────→ │    Node 3:3      │  ───────────────→ │     TAIL     │
│       │  (dummy)     │                   │    key = 4       │                   │    key = 3       │                   │  (dummy)     │
│       │              │  ←─────────────── │    value = 4     │  ←─────────────── │    value = 3     │  ←─────────────── │              │
│       └──────────────┘       prev        │    NEW! ⭐        │       prev        └──────────────────┘       prev        └──────────────┘
│                                          └──────────────────┘                             ↑ LRU                                          │
│                                                   ↑ MRU (Most Recently Used)       (Least Recently Used - Next to evict)                  │
│                                                (Just added!)                                                                              │
│                                                                                                                                 │
│                                                                                                                                 │
│   Node(1:1) EVICTED! ❌                                                                                                         │
│   ─────────────────────                                                                                                        │
│   • Removed from doubly linked list (tail.prev disconnected)                                                                   │
│   • Deleted from HashMap (key 1 no longer exists)                                                                              │
│   • Memory freed                                                                                                                │
│                                                                                                                                 │
│                                                                                                                                 │
│   HashMap Final State:                                                                                                         │
│   ────────────────────                                                                                                         │
│       ┌────────────────────────────────────────────────────────────────────┐                                                   │
│       │  Key 4  ───────────────┘ (points to Node 4:4 in DLL - MRU)        │                                                   │
│       │  Key 3  ────────────────────────────────────┘ (points to Node 3:3) │                                                   │
│       │  Key 1  DELETED! ❌ (was evicted)                                  │                                                   │
│       └────────────────────────────────────────────────────────────────────┘                                                   │
│                                                                                                                                 │
│   Cache Statistics:                                                                                                            │
│      ✅ Size: 2 / 2 (at capacity after eviction)                                                                               │
│      ✅ MRU (Most Recent): key=4 (just added)                                                                                  │
│      ✅ LRU (Least Recent): key=3 (will be evicted next if capacity exceeded)                                                  │
│                                                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
                                                      FINAL STATE SUMMARY
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                  COMPLETE SYSTEM STATE                                                          │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                                 │
│  Doubly Linked List (Visual Representation):                                                                                   │
│  ────────────────────────────────────────────                                                                                  │
│                                                                                                                                 │
│       ┌──────────────┐                ┌──────────────────┐                ┌──────────────────┐                ┌──────────────┐
│       │     HEAD     │  ←──────────→  │    Node 4:4      │  ←──────────→  │    Node 3:3      │  ←──────────→  │     TAIL     │
│       │  (dummy)     │                │    ⭐ MRU        │                │    ⚠️  LRU       │                │  (dummy)     │
│       └──────────────┘                └──────────────────┘                └──────────────────┘                └──────────────┘
│                                                ↑                                    ↑                                           │
│                                                │                                    │                                           │
│                                                │                                    │                                           │
│  HashMap (Key → Node References):              │                                    │                                           │
│  ─────────────────────────────────             │                                    │                                           │
│       ┌────────────────────────────────────────────────────────────────────────────────────┐                                   │
│       │  Key 4  ───────────────────────────────┘                                    │      │                                   │
│       │  Key 3  ────────────────────────────────────────────────────────────────────┘      │                                   │
│       └────────────────────────────────────────────────────────────────────────────────────┘                                   │
│                                                                                                                                 │
│  Cache Statistics:                                                                                                             │
│  ──────────────────                                                                                                            │
│      ✓ Current size: 2 / 2 (FULL - at maximum capacity)                                                                        │
│      ✓ Most Recently Used (MRU): Key 4 (last accessed/added)                                                                   │
│      ✓ Least Recently Used (LRU): Key 3 (next candidate for eviction)                                                          │
│                                                                                                                                 │
│  Eviction History:                                                                                                             │
│  ──────────────────                                                                                                            │
│      1. Key 2 evicted after put(3,3) - was LRU at that time                                                                    │
│      2. Key 1 evicted after put(4,4) - was LRU at that time                                                                    │
│                                                                                                                                 │
│  Complete Access Pattern Summary:                                                                                              │
│  ─────────────────────────────────                                                                                             │
│                                                                                                                                 │
│      put(1,1) → put(2,2) → get(1) → put(3,3) → get(2) → put(4,4)                                                              │
│                               ↑          ↑         ↑         ↑                                                                 │
│                          moved 1 to   evicted 2  returned  evicted 1                                                           │
│                             MRU                     -1                                                                          │
│                                                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
                                                  WHY O(1) TIME COMPLEXITY?
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

OPERATION BREAKDOWN:

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ get(key) — Time Complexity Analysis:                                                                                           │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                                 │
│   ✅ HashMap lookup: O(1) — Direct hash table access to find node                                                              │
│                                                                                                                                 │
│   ✅ _remove(node): O(1) — Update exactly 4 pointers to remove node from current position                                      │
│      Code:                                                                                                                      │
│        node.prev.next = node.next  (update left neighbor's next pointer)                                                       │
│        node.next.prev = node.prev  (update right neighbor's prev pointer)                                                      │
│                                                                                                                                 │
│   ✅ _add_to_head(node): O(1) — Update exactly 4 pointers to insert at MRU position                                            │
│      Code:                                                                                                                      │
│        node.next = head.next       (point to current first node)                                                               │
│        node.prev = head            (point back to head)                                                                        │
│        head.next.prev = node       (update old first node's prev)                                                              │
│        head.next = node            (update head's next)                                                                        │
│                                                                                                                                 │
│   ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── │
│   TOTAL: O(1) ✅ — Constant number of operations regardless of cache size                                                      │
│                                                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ put(key, value) — Time Complexity Analysis:                                                                                    │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                                 │
│   ✅ HashMap lookup: O(1) — Check if key already exists in cache                                                               │
│                                                                                                                                 │
│   ✅ Create node: O(1) — Allocate new Node object with key and value                                                           │
│                                                                                                                                 │
│   ✅ HashMap insert: O(1) — Add key → node mapping to hash table                                                               │
│                                                                                                                                 │
│   ✅ _add_to_head(node): O(1) — Update 4 pointers to insert at MRU position                                                    │
│                                                                                                                                 │
│   ✅ _remove_tail(): O(1) — Remove LRU node when capacity exceeded                                                             │
│      Code:                                                                                                                      │
│        lru = tail.prev             (O(1) — direct reference to LRU node!)                                                      │
│        _remove(lru)                (O(1) — 4 pointer updates)                                                                  │
│                                                                                                                                 │
│   ✅ HashMap delete: O(1) — Remove evicted key from hash table                                                                 │
│                                                                                                                                 │
│   ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── │
│   TOTAL: O(1) ✅ — Constant number of operations regardless of cache size                                                      │
│                                                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ KEY INSIGHT: Why Doubly Linked List enables O(1) removal?                                                                      │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                                 │
│  Removal from MIDDLE of list — The critical difference:                                                                        │
│  ────────────────────────────────────────────────────────                                                                      │
│                                                                                                                                 │
│      Singly Linked List: O(N) — Must traverse from head to find previous node                                                  │
│      Doubly Linked List: O(1) — node.prev gives instant access to previous node!                                               │
│                                                                                                                                 │
│  Example: Remove Node [1:1] from: HEAD ↔ [3:3] ↔ [1:1] ↔ [2:2] ↔ TAIL                                                         │
│  ────────────────────────────────────────────────────────────────────────────                                                  │
│                                                                                                                                 │
│      Singly Linked List Approach (SLOW):                                                                                       │
│      ────────────────────────────────────                                                                                      │
│        ❌ Step 1: Start at head, traverse: head → 3 → 1 (found!)                                                               │
│        ❌ Step 2: Need to update node 3's next pointer... but we don't have reference to node 3!                               │
│        ❌ Step 3: Must traverse AGAIN from head to find node 3                                                                 │
│        ❌ Time: O(N) — Must traverse list to find predecessor                                                                  │
│                                                                                                                                 │
│      Doubly Linked List Approach (FAST):                                                                                       │
│      ─────────────────────────────────────                                                                                     │
│        ✅ Step 1: Have direct node reference from HashMap                                                                      │
│        ✅ Step 2: node.prev.next = node.next  (update left neighbor — instant access via prev!)                                │
│        ✅ Step 3: node.next.prev = node.prev  (update right neighbor — instant access via next!)                               │
│        ✅ Done in exactly 2 pointer updates!                                                                                   │
│        ✅ Time: O(1) — No traversal needed!                                                                                    │
│                                                                                                                                 │
│  This is why LRU Cache MUST use Doubly Linked List! The prev pointer is essential for O(1) removal.                            │
│                                                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
"""

# ============================================================================
#              🎯 MEMORY TRICKS & COMMON MISTAKES
# ============================================================================

"""
🧠 HOW TO REMEMBER THIS SOLUTION:
---------------------------------
1. "FIND AND ORDER" → HashMap finds, DLL orders
2. "DUMMY GUARDS" → Dummy head/tail eliminate edge cases
3. "DOUBLY NOT SINGLY" → Need prev pointer for O(1) removal
4. "MOVE ON ACCESS" → Both get() and put() move to head!

❌ COMMON MISTAKES TO AVOID:
----------------------------
1. ❌ Using singly linked list
      WRONG: Can't remove from middle in O(1)
      RIGHT: Doubly linked list with prev pointers

2. ❌ Not using dummy nodes
      WRONG: Complex edge cases (empty list, single element)
      RIGHT: Dummy head and tail simplify all operations

3. ❌ Forgetting to update HashMap when removing
      WRONG: Remove from DLL but not HashMap
      RIGHT: del cache[key] when removing from DLL

4. ❌ Not moving node on get()
      WRONG: get() just returns value
      RIGHT: get() moves node to head (marks as MRU)

5. ❌ Not moving to head when updating existing key
      WRONG: put() existing key only updates value
      RIGHT: put() updates value AND moves to head

6. ❌ Removing wrong node
      WRONG: Remove from head when evicting
      RIGHT: Remove from tail (tail.prev is LRU)

7. ❌ Checking capacity before adding
      WRONG: if len(cache) == capacity: evict, then add
      RIGHT: Add first, then if len(cache) > capacity: evict
      (Otherwise can't update existing keys when at capacity!)

✅ PRO TIPS:
-----------
1. Draw the DLL structure before coding
2. Test edge cases: capacity=1, updating existing key
3. OrderedDict is simpler but may not be allowed
4. Dummy nodes are CRITICAL - don't skip them!
5. Always update BOTH HashMap and DLL together

🎯 INTERVIEW STRATEGY:
---------------------
"I'll use a HashMap for O(1) access and a doubly linked list to maintain
LRU order. The HashMap maps keys to nodes in the DLL. The DLL has dummy
head and tail nodes to simplify edge cases. head.next is the most recently
used, tail.prev is least recently used. On get(), I move the node to head.
On put(), if capacity is exceeded, I remove tail.prev and delete from HashMap."

Then code it step by step, explaining the helper methods first!
"""

# ============================================================================
#                         🧪 TEST CASES
# ============================================================================

if __name__ == "__main__":
    print("="*80)
    print("                  LRU CACHE - TEST CASES")
    print("="*80)

    # Test Case 1: Standard operations
    print("\n📝 Test Case 1: Standard operations (capacity=2)")
    print("-" * 80)
    cache1 = LRUCache(2)

    print("put(1, 1)")
    cache1.put(1, 1)
    print("put(2, 2)")
    cache1.put(2, 2)
    result1 = cache1.get(1)
    print(f"get(1) = {result1}")
    print("Expected: 1")
    print(f"✅ PASS" if result1 == 1 else "❌ FAIL")

    print("\nput(3, 3)  # Evicts key 2")
    cache1.put(3, 3)
    result2 = cache1.get(2)
    print(f"get(2) = {result2}")
    print("Expected: -1 (evicted)")
    print(f"✅ PASS" if result2 == -1 else "❌ FAIL")

    print("\nput(4, 4)  # Evicts key 1")
    cache1.put(4, 4)
    result3 = cache1.get(1)
    print(f"get(1) = {result3}")
    print("Expected: -1 (evicted)")
    print(f"✅ PASS" if result3 == -1 else "❌ FAIL")

    result4 = cache1.get(3)
    print(f"get(3) = {result4}")
    print("Expected: 3")
    print(f"✅ PASS" if result4 == 3 else "❌ FAIL")

    result5 = cache1.get(4)
    print(f"get(4) = {result5}")
    print("Expected: 4")
    print(f"✅ PASS" if result5 == 4 else "❌ FAIL")

    # Test Case 2: Update existing key
    print("\n📝 Test Case 2: Update existing key")
    print("-" * 80)
    cache2 = LRUCache(2)
    cache2.put(1, 1)
    cache2.put(2, 2)
    print("put(1, 1), put(2, 2)")

    cache2.put(1, 10)
    print("put(1, 10)  # Update key 1")
    result6 = cache2.get(1)
    print(f"get(1) = {result6}")
    print("Expected: 10")
    print(f"✅ PASS" if result6 == 10 else "❌ FAIL")

    cache2.put(3, 3)
    print("\nput(3, 3)  # Should evict 2, not 1 (1 was just updated)")
    result7 = cache2.get(2)
    print(f"get(2) = {result7}")
    print("Expected: -1 (evicted)")
    print(f"✅ PASS" if result7 == -1 else "❌ FAIL")

    # Test Case 3: Capacity of 1
    print("\n📝 Test Case 3: Single capacity")
    print("-" * 80)
    cache3 = LRUCache(1)
    cache3.put(1, 1)
    print("put(1, 1)")

    cache3.put(2, 2)
    print("put(2, 2)  # Evicts 1")
    result8 = cache3.get(1)
    print(f"get(1) = {result8}")
    print("Expected: -1 (evicted)")
    print(f"✅ PASS" if result8 == -1 else "❌ FAIL")

    result9 = cache3.get(2)
    print(f"get(2) = {result9}")
    print("Expected: 2")
    print(f"✅ PASS" if result9 == 2 else "❌ FAIL")

    # Test Case 4: Multiple gets
    print("\n📝 Test Case 4: Multiple gets of same key")
    print("-" * 80)
    cache4 = LRUCache(2)
    cache4.put(1, 1)
    cache4.put(2, 2)
    print("put(1, 1), put(2, 2)")

    cache4.get(1)
    cache4.get(1)
    cache4.get(1)
    print("get(1) × 3 times  # 1 becomes MRU")

    cache4.put(3, 3)
    print("put(3, 3)  # Should evict 2, not 1")
    result10 = cache4.get(2)
    print(f"get(2) = {result10}")
    print("Expected: -1 (evicted)")
    print(f"✅ PASS" if result10 == -1 else "❌ FAIL")

    result11 = cache4.get(1)
    print(f"get(1) = {result11}")
    print("Expected: 1")
    print(f"✅ PASS" if result11 == 1 else "❌ FAIL")

    # Test Case 5: OrderedDict implementation
    print("\n📝 Test Case 5: OrderedDict implementation")
    print("-" * 80)
    cache5 = LRUCache_OrderedDict(2)
    cache5.put(1, 1)
    cache5.put(2, 2)
    print("put(1, 1), put(2, 2)")

    result12 = cache5.get(1)
    print(f"get(1) = {result12}")
    print("Expected: 1")
    print(f"✅ PASS" if result12 == 1 else "❌ FAIL")

    cache5.put(3, 3)
    print("put(3, 3)  # Evicts 2")
    result13 = cache5.get(2)
    print(f"get(2) = {result13}")
    print("Expected: -1")
    print(f"✅ PASS" if result13 == -1 else "❌ FAIL")

    # Test Case 6: Large capacity
    print("\n📝 Test Case 6: Larger capacity (capacity=5)")
    print("-" * 80)
    cache6 = LRUCache(5)
    for i in range(1, 6):
        cache6.put(i, i * 10)
    print("put(1,10), put(2,20), put(3,30), put(4,40), put(5,50)")

    cache6.get(3)
    cache6.get(5)
    print("get(3), get(5)  # 3 and 5 become MRU")

    cache6.put(6, 60)
    print("put(6, 60)  # Should evict 1 (LRU)")
    result14 = cache6.get(1)
    print(f"get(1) = {result14}")
    print("Expected: -1 (evicted)")
    print(f"✅ PASS" if result14 == -1 else "❌ FAIL")

    result15 = cache6.get(3)
    print(f"get(3) = {result15}")
    print("Expected: 30")
    print(f"✅ PASS" if result15 == 30 else "❌ FAIL")

    print("\n" + "="*80)
    print("              ✅ ALL TEST CASES COMPLETED!")
    print("="*80)


# ============================================================================
#              🎓 LEARNING SUMMARY & KEY TAKEAWAYS
# ============================================================================

"""
🎯 WHAT YOU LEARNED:
-------------------
1. LRU Cache requires O(1) operations → HashMap + DLL!
2. HashMap provides O(1) access to nodes
3. Doubly Linked List provides O(1) reordering
4. Dummy head/tail eliminate edge cases
5. Must update BOTH HashMap and DLL together!

🔑 KEY PATTERN: "HashMap + Doubly Linked List"
-----------------------------------------------
This pattern applies when:
- Need O(1) access to elements
- Need O(1) insertion/deletion
- Need to maintain order
- Need to track "most/least recently used"

Used in:
- LRU Cache (this problem!)
- LFU Cache (LeetCode #460)
- All O(1) Data Structure (LeetCode #432)
- Browser back/forward buttons
- Operating system page replacement

💪 THREE APPROACHES TO MASTER:
-----------------------------
1. HASHMAP + DLL (Optimal - O(1))
   - HashMap: key → Node
   - DLL: head ↔ ... ↔ tail (MRU to LRU)
   - Dummy nodes eliminate edge cases
   - Industry standard implementation

2. ORDEREDDICT (Python - O(1))
   - Built-in Python data structure
   - Maintains insertion order
   - move_to_end() and popitem() are O(1)
   - Simpler but language-specific

3. ARRAY WITH TIMESTAMPS (Bad - O(N))
   - Shows WHY HashMap + DLL is needed
   - All operations become O(N)
   - Violates problem requirements
   - Educational only!

🎯 INTERVIEW TIPS:
-----------------
1. Clarify requirements:
   - Does get() count as "use"? (YES!)
   - Should put() existing key move to head? (YES!)
   - What to return if key doesn't exist? (-1)

2. Explain data structure choice:
   - HashMap alone can't track order
   - List alone can't find items in O(1)
   - DLL allows O(1) removal from anywhere
   - Dummy nodes simplify edge cases

3. Draw the structure:
   - Show HashMap and DLL together
   - Label MRU and LRU positions
   - Demonstrate pointer updates

4. Test edge cases:
   - Capacity of 1
   - Updating existing key
   - Multiple gets of same key
   - Empty cache

5. Mention real-world uses:
   - Web browser cache
   - Database query cache
   - CDN caching
   - OS memory management

🎉 CONGRATULATIONS!
------------------
You now understand how to implement LRU Cache with O(1) operations!
Remember: "HashMap finds it, Doubly Linked List orders it!"

📊 COMPLEXITY SUMMARY:
---------------------
┌────────────────────┬──────────────┬──────────────┐
│ Approach           │ Time         │ Space        │
├────────────────────┼──────────────┼──────────────┤
│ HashMap + DLL      │ O(1)         │ O(capacity)  │
│ OrderedDict        │ O(1)         │ O(capacity)  │
│ Array (Bad)        │ O(N)         │ O(capacity)  │
└────────────────────┴──────────────┴──────────────┘

🏆 RECOMMENDED: Use HashMap + Doubly Linked List for optimal O(1) solution!

🔗 RELATED PROBLEMS TO PRACTICE:
-------------------------------
1. LeetCode #146: LRU Cache (this problem!)
2. LeetCode #460: LFU Cache (Least Frequently Used)
3. LeetCode #432: All O(1) Data Structure
4. LeetCode #380: Insert Delete GetRandom O(1)
5. LeetCode #381: Insert Delete GetRandom O(1) - Duplicates allowed

💡 FINAL TIP:
------------
LRU Cache is one of the MOST IMPORTANT interview problems! It tests:
- Data structure knowledge (HashMap, Linked List)
- Pointer manipulation
- Edge case handling
- System design thinking

Master this problem thoroughly - it appears in 95% of system design interviews
at top tech companies! The pattern of "HashMap + DLL for O(1) operations"
is fundamental and appears in many other problems!
"""
