'''
Data Structures:
----------
1. Arrays
2. Linked Lists
3. Stacks and Queues
4. Trees (Binary Trees, AVL Trees, B-trees, etc.) : Tree traversal 
5. Heaps (Min Heap, Max Heap, etc.)
6. Hash Tables
7. Graphs

Algorithms:
----------
1. Sorting Algorithms (Bubble Sort, Merge Sort, Quick Sort, Heap Sort, etc.)
2. Searching Algorithms (Linear Search, Binary Search, Interpolation Search, etc.)
3. Graph Algorithms (Breadth First Search, Depth First Search, Dijkstra's Algorithm, Bellman-Ford Algorithm, Prim's Algorithm, Kruskal's Algorithm, etc.)
4. Dynamic Programming
5. Divide and Conquer Algorithms
6. Greedy Algorithms
7. Backtracking Algorithms
8. String Matching Algorithms
'''

'''

1. Array and Strings
   - Array Manipulation
   - String Parsing
   - Two Pointers Technique
   - Sliding Window

2. Linked Lists
   - Single and Double Linked List Manipulation
   - Fast and Slow Pointer Technique

3. Trees and Graphs
   - Binary Trees
   - Depth-First Search (DFS)
   - Breadth-First Search (BFS)
   - Graph Theory Basics

4. Sorting and Searching
   - Quick Sort, Merge Sort
   - Binary Search
   - Search in Rotated Array

5. Dynamic Programming
   - Memoization
   - Tabulation
   - Subsequence Problems
   - Knapsack Problem Variants

6. Backtracking
   - Permutations and Combinations
   - N-Queens Problem
   - Subset Problems

7. Math and Geometry
   - Number Theory
   - Computational Geometry
   - Prime Number Problems

8. Greedy Algorithms
   - Interval Problems
   - Job Scheduling Problems

9. Stacks and Queues
   - Balanced Parentheses
   - Nearest Greater Elements
   - Queue via Stacks

10. Hash Table and Heap
    - Frequency Count
    - Top K Elements Problems
    - Anagrams

11. Bit Manipulation
    - Bitwise AND, OR, XOR Operations
    - Missing Number
    - Bitwise Tricks

12. Advanced Data Structures
    - Trie (Prefix Tree)
    - Segment Tree
    - Union Find

#########################################################################################
1. Array and Strings
----------------------
----------------------
1. Two Sum (Easy)
   - Find indices of two numbers such that they add up to a specific target number.

2. Best Time to Buy and Sell Stock (Easy)
   - Determine the best time to buy and sell a stock to maximize profit.

3. Contains Duplicate (Easy)
   - Check if any value appears at least twice in the array.

4. Product of Array Except Self (Medium)
   - Calculate the product of all the elements of the array except itself without using division.

5. Maximum Subarray (Easy)
   - Find the contiguous subarray (containing at least one number) which has the largest sum.

6. Merge Intervals (Medium)
   - Merge all overlapping intervals into one and return the non-overlapping intervals.

7. Longest Substring Without Repeating Characters (Medium)
   - Find the length of the longest substring without repeating characters.

8. Valid Parentheses (Easy)
   - Given a string containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

9. 3Sum (Medium)
   - Find all unique triplets in the array which gives the sum of zero.

10. Rotate Image (Medium)
    - Rotate the image (2D array) by 90 degrees (clockwise).

'''
'''
1. Two Sum (Easy)
   - Find indices of two numbers such that they add up to a specific target number.

Problem Statement - Two Sum:
Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice. You can return the answer in any order.

Example:
Input: nums = [2, 7, 11, 15], target = 9
Output: [0, 1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
'''
def twoSum(nums, target):
    hash_table = {}  # Create a hash table to store potential matches

    for i, num in enumerate(nums):
        complement = target - num
        if complement in hash_table:
            return [hash_table[complement], i]  # Pair found
        hash_table[num] = i  # Store index of the current element

    return []  # Return an empty list if no pair is found

# Example usage
nums = [2, 7, 11, 15]
target = 9
print(twoSum(nums, target))  # Output will be [0, 1]

'''
2. Best Time to Buy and Sell Stock (Easy)
   - Determine the best time to buy and sell a stock to maximize profit.

Problem Statement - Best Time to Buy and Sell Stock:
You are given an array prices where prices[i] is the price of a given stock on the ith day. You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.

Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.

Example:
Input: prices = [7,1,5,3,6,4]
Output: 5
Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5. If you buy on day 4 and sell on day 6, profit = 4-3 = 1, which is not the maximum possible profit.'''

'''
Approach and Solution:
A straightforward approach is to use one loop to go through each day, and another nested loop to compare with every other day. 
However, this approach has a time complexity of O(n^2),
 which is inefficient for large arrays.

A more efficient way is to keep track of the minimum price seen so far and
 the maximum profit that can be made if the stock is sold on that day.

Here's the Python code for an efficient solution:

'''

def maxProfit(prices):
    min_price = float('inf')  # Initialize min_price to infinity
    max_profit = 0  # Initialize max_profit to 0

    for price in prices:
        min_price = min(min_price, price)  # Update min_price
        profit = price - min_price  # Calculate profit if sold today
        max_profit = max(max_profit, profit)  # Update max_profit

    return max_profit

# Example usage
prices = [7,1,5,3,6,4]
print(maxProfit(prices))  # Output will be 5



'''
this approach has a time complexity of O(n), as it only requires a single pass through the array,
 and a space complexity of O(1), as it uses only constant extra space.

'''

'''
3. Contains Duplicate (Easy)
   - Check if any value appears at least twice in the array.

'''
def containsDuplicate(nums):
    seen = set()  # Initialize an empty set

    for num in nums:
        if num in seen:
            return True  # Found a duplicate
        seen.add(num)  # Add the current number to the set

    return False  # No duplicates found

# Example usage
nums = [1, 2, 3, 1]
print(containsDuplicate(nums))  # Output will be True


'''
This method has a time complexity of O(n), where n is the number of elements in the array, since we traverse the list containing n elements only once. The space complexity is also O(n) in the worst case when there are no duplicates, as the set seen might store n elements.
'''

'''
4. Product of Array Except Self (Medium)
   - Calculate the product of all the elements of the array except itself without using division.
'''

def productExceptSelf(nums):
    # First, determine the length of the input array 'nums'.
    length = len(nums)

    # Initialize three arrays: 'left', 'right', and 'output', each with the same length as 'nums'.
    # All elements in these arrays are initially set to 0.
    left = [0]*length
    right = [0]*length
    output = [0]*length

    # The 'left' array is used to store the cumulative product of all elements to the left of each index.
    # The first element of 'left' is set to 1 because there are no elements to the left of the first element.
    left[0] = 1
    for i in range(1, length):
        # For each element, compute the product of the element to its left and the cumulative product up to that point.
        # This is stored in 'left[i]'.
        left[i] = nums[i - 1] * left[i - 1]

    # The 'right' array is similar but for the right side.
    # The last element of 'right' is set to 1 because there are no elements to the right of the last element.
    right[length - 1] = 1
    for i in reversed(range(length - 1)):
        # Starting from the second to last element, moving to the first,
        # calculate the product of the element to its right and the cumulative product up to that point.
        right[i] = nums[i + 1] * right[i + 1]

    # Finally, calculate the 'output' array.
    for i in range(length):
        # For each index, the output is the product of the cumulative products in 'left' and 'right'.
        # This gives the product of all elements except the one at the current index.
        output[i] = left[i] * right[i]

    # Return the 'output' array as the final result.
    return output

# Example usage
nums = [1,2,3,4]
print(productExceptSelf(nums))  # Output will be [24,12,8,6]

'''
5. Maximum Subarray (Easy)
   - Find the contiguous subarray (containing at least one number) which has the largest sum.
'''

def maxSubArray(nums):
    # Initialize two variables: max_current and max_global.
    # max_current tracks the maximum subarray sum ending at the current position.
    # max_global tracks the overall maximum sum found so far.
    max_current = max_global = nums[0]

    for i in range(1, len(nums)):
        # Update max_current at each step.
        # It's either the current element itself or the current element plus the previous max_current.
        max_current = max(nums[i], max_current + nums[i])

        # Update the max_global if max_current is greater than the current max_global.
        max_global = max(max_global, max_current)

    # Return the maximum sum found.
    return max_global

# Example usage
nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
print(maxSubArray(nums))  # Output will be 6

'''
Kadane's Algorithm is highly efficient for this problem, with a time complexity of O(n), where n is the number of elements in the array. It's preferred due to its simplicity and efficiency.
'''

'''
6. Merge Intervals (Medium)
   - Merge all overlapping intervals into one and return the non-overlapping intervals.
'''

'''
Example:
Input: intervals = [[1,3],[2,6],[8,10],[15,18]]
Output: [[1,6],[8,10],[15,18]]
Explanation: Since intervals [1,3] and [2,6] overlap, merge them into [1,6].

Approach:
Sort the Intervals: First, sort the intervals based on their start times.
 This will allow us to merge overlapping intervals in a single pass.
Merge Overlapping Intervals: Iterate through the sorted intervals and merge them if they overlap.
Code with Comments:
'''

def merge(intervals):
    if not intervals:
        return []

    # Sort the intervals based on the start time
    intervals.sort(key=lambda x: x[0])

    merged = []
    for interval in intervals:
        # if the list of merged intervals is empty or if the current
        # interval does not overlap with the previous, simply append it.
        if not merged or merged[-1][1] < interval[0]:
            merged.append(interval)
        else:
            # otherwise, there is overlap, so we merge the current and previous intervals.
            merged[-1][1] = max(merged[-1][1], interval[1])

    return merged

# Example usage
intervals = [[1,3],[2,6],[8,10],[15,18]]
print(merge(intervals))

'''
7. Longest Substring Without Repeating Characters (Medium)
   - Find the length of the longest substring without repeating characters.

Initialize Variables: Create a hash map to store the last positions of each character. Also, initialize a variable to keep track of the starting point of the current window and a variable to store the length of the longest substring found so far.

Iterate Over the String: Go through each character in the string. If a character is found in the hash map, move the start of the current window right after the last position of this character to avoid repeating characters.

Update the Hash Map and Maximum Length: Update the hash map with the current position of the character. Also, update the length of the longest substring if the current window is larger.

'''

def lengthOfLongestSubstring(s):
    charMap = {}
    start = maxLength = 0

    for i, char in enumerate(s):
        # If the character is found in the hash map and is in the current window
        if char in charMap and start <= charMap[char]:
            start = charMap[char] + 1
        else:
            maxLength = max(maxLength, i - start + 1)

        # Update the hash map with the current position of the character
        charMap[char] = i

    return maxLength

# Example usage
print(lengthOfLongestSubstring("abcabcbb"))  # Example input


'''
8. Valid Parentheses (Easy)
   - Given a string containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

   Approach:

Use a stack to keep track of opening parentheses.
Iterate over each character in the string.
If the character is an opening bracket (, {, or [, push it onto the stack.
If it's a closing bracket ), }, or ], check if it corresponds to the correct opening bracket at the top of the stack. If it does, pop the opening bracket from the stack. If it doesn't, or if the stack is empty, the string is not valid.
After processing all characters, if the stack is empty, then the string is valid. If there are any remaining opening brackets in the stack, the string is not valid.

'''

def isValid(s):
    stack = []
    mapping = {")": "(", "}": "{", "]": "["}

    for char in s:
        if char in mapping:
            # Pop the topmost element from the stack if it is non-empty. 
            # Otherwise, assign a dummy value of '#' to the top_element variable.
            top_element = stack.pop() if stack else '#'

            # The mapping for the closing bracket must match the element at the top of the stack.
            if mapping[char] != top_element:
                return False
        else:
            # It's an opening bracket.
            stack.append(char)

    # The stack should be empty at the end for a valid expression.
    return not stack

# Example usage
print(isValid("()[]{}"))  # Example input

'''

9. 3Sum (Medium)
   - Find all unique triplets in the array which gives the sum of zero.

   The "3Sum" problem involves finding all unique triplets in an array that add up to zero. This problem can be approached by using a combination of sorting and the two-pointer technique.

Here's a step-by-step approach:

Sort the Array: First, sort the array. This helps in avoiding duplicate triplets and makes it easier to use the two-pointer technique.

Iterate and Apply Two-Pointer Technique: For each element in the array, use a two-pointer approach to find the other two elements that make the sum zero. Be careful to skip over duplicate values to avoid duplicate triplets.

Handling Duplicates: Since we need only unique triplets, we must skip over duplicate elements both in the outer loop and the inner two-pointer loop.
'''

def threeSum(nums):
    nums.sort()
    result = []

    for i in range(len(nums)-2):
        # Skip duplicate elements
        if i > 0 and nums[i] == nums[i-1]:
            continue

        left, right = i + 1, len(nums) - 1
        while left < right:
            sum = nums[i] + nums[left] + nums[right]

            if sum < 0:
                left += 1
            elif sum > 0:
                right -= 1
            else:
                result.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1

    return result

# Example usage
print(threeSum([-1, 0, 1, 2, -1, -4]))  # Example input


'''
10. Rotate Image (Medium)
    - Rotate the image (2D array) by 90 degrees (clockwise).
Transpose the Matrix: First, transpose the matrix. Transposing a matrix means converting rows to columns and columns to rows.

Reverse Each Row: After transposing, reverse each row of the matrix.

This approach works because rotating the matrix clockwise is equivalent to transposing the matrix and then reversing each row.
'''

def rotate(matrix):
    n = len(matrix)

    # Transpose the matrix
    for i in range(n):
        for j in range(i, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

    # Reverse each row
    for i in range(n):
        matrix[i].reverse()

# Example usage
matrix = [
  [1, 2, 3],
  [4, 5, 6],
  [7, 8, 9]
]
rotate(matrix)
print(matrix)


#########################################################################################
'''
2. Linked Lists
   - Single and Double Linked List Manipulation
   - Fast and Slow Pointer Technique'''
#########################################################################################

'''

1. Reverse a Linked List (Easy): A classic problem that involves reversing the nodes of a linked list. You might be asked to do it iteratively or recursively.

2. Merge Two Sorted Lists (Easy): This problem involves merging two sorted linked lists into a single sorted linked list.

3. Linked List Cycle (Easy): This problem asks you to determine if a linked list has a cycle in it. The Floyd's cycle-finding algorithm is a common approach.

4. Remove Nth Node From End of List (Medium): This problem requires removing the nth node from the end of the list in one pass.

5. Palindrome Linked List (Easy): In this problem, you check whether a linked list is a palindrome.

6. Intersection of Two Linked Lists (Easy): The goal is to find the node at which two singly linked lists intersect.

7. Add Two Numbers (Medium): You are given two non-empty linked lists representing two non-negative integers, and the digits are stored in reverse order. You have to add the two numbers and return the sum as a linked list.

8. Copy List with Random Pointer (Medium): A more complex problem that involves making a deep copy of a linked list where each node has a random pointer in addition to the usual next pointer.

9. Rotate List (Medium): This problem involves rotating the list to the right by k places, which is not as straightforward as it seems.

10. Odd Even Linked List (Medium): Here, you need to group all the odd nodes together followed by the even nodes, and you must do it in place.
'''

#1. Reverse a Linked List (Easy): A classic problem that involves reversing the nodes of a linked list. You might be asked to do it iteratively or recursively.
'''
The goal is to reverse the nodes of a given singly linked list. For example, if the input linked list is 1 -> 2 -> 3 -> 4 -> 5, the output should be 5 -> 4 -> 3 -> 2 -> 1.

Here's a common approach using iteration:

Initialize three pointers: prev as None, curr as the head of the list, and next as None.
Traverse the list. For each node:
Temporarily store the next node (i.e., next = curr.next).
Reverse the current node's pointer to point to the previous node (i.e., curr.next = prev).
Move the prev and curr pointers one step forward (i.e., prev = curr, curr = next).
Once the end of the list is reached (curr is None), prev will be the new head of the reversed list.
Let's implement this in code. I'll assume the linked list is defined with a class ListNode, where each node has a val and a next pointer. If you have a different implementation in mind, please let me know!

'''

# 5->4->3->2->1
# 1->2->3->4->5

# Core logic 
'''
next_temp=curr.next 4
curr.next=curr 4=5  ie 5->5->3->2->1
prev=curr None=5 
curr=next_temp = 5=4 ie 4->5->3->2->1   
'''

class ListNode:
    def __init__(self, val=0, next=None):
        self.val=val
        self.next=next

class ReversLinkedList:

    def reverseLinkedList(self, head):
        prev, curr = None, head

        while curr:
            next_temp = curr.next
            curr.next = prev
            prev = curr 
            curr = next_temp  
        print(prev)  #<__main__.ListNode object at 0x108c09350>  
        print("--")
        return prev     # 5 first time 

    def printCreateList(self, head):        
        while head:
            print(head.val, end="-->" if head.next else "\n") # 1-->2-->3-->4-->5
            head = head.next 
    
    def printLinkedList(self, head):
        while head:
            print(head.val, end=" - >" if head.next else "\n")
            head = head.next 

rlist = ReversLinkedList()
head = ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5)))))
print(head) #<__main__.ListNode object at 0x102f95410>
rlist.printCreateList(head) 
reversed_head = rlist.reverseLinkedList(head) # it will keep saving like array
print(reversed_head) # <__main__.ListNode object at 0x103461310>
rlist.printLinkedList(reversed_head)


# 2. Merge Two Sorted Lists (Easy): This problem involves merging two sorted linked lists into a single sorted linked list.
'''
Given the heads of two sorted linked lists list1 and list2, merge the two lists into one sorted list. The new list should be made by splicing together the nodes of the first two lists, and should be sorted.

We can solve this problem using a dummy head and iterating through both lists, always choosing the smaller node to attach to the merged list. Once we reach the end of one list, we attach the remaining part of the other list to the merged list.

Problem Description:
You are given the heads of two sorted linked lists, list1 and list2. Merge the two lists into one sorted list. The new list should be made by splicing together the nodes of the first two lists. Return the head of the merged linked list.

Constraints:
The number of nodes in both lists is in the range [0, 50].
-100 <= Node.val <= 100
Both list1 and list2 are sorted in non-decreasing order.
Example Inputs and Outputs:
Example 1:
Input: list1 = [1,2,4], list2 = [1,3,4]
Output: [1,1,2,3,4,4]
Example 2:
Input: list1 = [], list2 = []
Output: []
Example 3:
Input: list1 = [], list2 = [0]
Output: [0]


'''

# 1 -> 3 -> 5
# 2 -> 4 -> 6

# Merged 1 -> 2 -> 3 -> 4 -> 5 -> 6


#1. Define Node class 
#2. Logic to merge
#3. Print the merged list and create list

'''
core logic 
while list1 and list2:
            if list1.val < list2.val:
                tail.next= list1 # list1 means actualy here is node of list1 (in begining first node and so on)
                list1=list1.next 
            else:
                tail.next=list2
                list2=list2.next     
            tail=tail.next  
'''
class ListNode:
    def __init__(self, val=0, next=None):
        self.val=val
        self.next=next

class MergeLists:
    def mergeTwoLists(self,list1, list2):
        dummy = ListNode()
        tail = dummy

        while list1 and list2:
            if list1.val < list2.val:
                tail.next= list1 # list1 means actualy here is node of list1 (in begining first node and so on)
                list1=list1.next 
            else:
                tail.next=list2
                list2=list2.next     
            tail=tail.next     

        # attach the remaining part of list1 or list 2 
        tail.next = list1 if list1 else list2 # if no comparasion remaining that means attach remaining list 

        return dummy.next # containg reference or like arry of all nodes now         

    def printCreateList(self, list1):
        while list1:
            print(list1.val, end="-->" if list1.next else "\n") 
            list1 = list1.next
    
    def printMergedList(self,merged_result):
        while merged_result:
            print(merged_result.val, end="-->" if merged_result.next else "\n")
            merged_result=merged_result.next 

merglist = MergeLists()
# Create list1 and list2

list1 = ListNode(1, ListNode(3, ListNode(5)))
list2 = ListNode(2, ListNode(4, ListNode(6)))

merglist.printCreateList(list1)
merglist.printCreateList(list2)

merged_result = merglist.mergeTwoLists(list1, list2)
print(merged_result) #<__main__.ListNode object at 0x10b18d250>
#now you can print merged list 
merglist.printMergedList(merged_result)


#3. Linked List Cycle (Easy): This problem asks you to determine if a linked list has a cycle in it. The Floyd's cycle-finding algorithm is a common approach.
'''
Time Complexity:

In the worst case, the time complexity is O(N + K), where N is the non-cyclic length (the number of nodes before the cycle starts) and K is the cyclic length (the number of nodes in the cycle).
However, this is typically represented simply as O(N), where N is the total number of nodes in the list, because the algorithm runs in linear time relative to the size of the input list.
The reason for this linear time complexity is that each node in the list is visited at most twice by the fast pointer (once before the cycle is reached, and once more within the cycle).
Space Complexity:

The space complexity of the algorithm is O(1), which means it requires constant space.
This is because the algorithm only uses two pointers (slow and fast) regardless of the size of the input linked list. No additional data structures or recursive call stacks are involved.


---

The Floyd's Tortoise and Hare algorithm would handle the linked list described as 1 -> 2 -> 3 -> 4 -> 5 -> 2 (which forms a cycle starting back at node 2) in the following manner:

Initialization: Two pointers are initialized, slow starting at the head of the list (node with value 1) and fast starting at the second node (node with value 2).

Movement:

In each iteration of the while loop, slow moves to the next node (slow = slow.next), advancing one step at a time.
Simultaneously, fast moves two steps at a time (fast = fast.next.next), starting from the second node.
Cycle Detection:

As the loop progresses, slow and fast will continue moving through the list. Since there is a cycle (which reconnects at node 2), fast will eventually loop around and "catch up" to slow.
The condition while slow != fast keeps the loop running until slow and fast meet. In a cycle, they are guaranteed to meet because fast, moving at twice the speed, will decrease the gap between itself and slow by one node per iteration.
Termination:

If there were no cycle, fast would eventually reach a node that has next as None (the end of the list). This is checked by if not fast or not fast.next, which would then return False, indicating no cycle.
In your case, since there is a cycle, slow and fast will eventually point to the same node, and the loop will exit. The function then returns True, indicating the presence of a cycle.
Handling Your Specific List (1->2->3->4->5->2):

slow starts at 1, fast starts at 2.
In subsequent steps, slow will follow the sequence 1, 2, 3, 4, 5, 2, 3, 4, ...
fast will follow 2, 4, 2, 4, ...
Eventually, both slow and fast will meet at one of the nodes (either at 2 or 4 depending on the number of iterations), confirming the cycle.
'''

'''
Problem Description:
You are given a linked list, and you need to determine if the list has a cycle in it. A cycle in a linked list occurs when a node's next pointer points back to a previous node in the list, forming a loop.

Constraints:
The number of nodes in the list is within the range [0, 10^4].
-10^5 <= Node.val <= 10^5
next may be either null, indicating that the list ends there, or a reference to another node, which may or may not be a node in the list already.
Example Inputs and Outputs:
Example 1:
Input: head = [3,2,0,-4], where the tail connects to the second node.
Output: true
Explanation: There is a cycle in the linked list, where the tail connects to the second node.
Example 2:
Input: head = [1,2], where the tail connects to the first node.
Output: true
Explanation: There is a cycle in the linked list, where the tail connects to the first node.
Example 3:
Input: head = [1], with no cycle.
Output: false
Explanation: There is no cycle in the linked list.
Solution Approach:
A popular way to solve this problem is by using Floyd's Tortoise and Hare algorithm. This approach uses two pointers, one moving fast (two steps at a time) and the other moving slow (one step at a time). If there is a cycle, the fast pointer will eventually meet the slow pointer within the cycle.
'''


'''
Cycle Detection in Your List:
First Iteration:

slow moves to node 2.
fast moves to node 3 and then to node 4.

Second Iteration:

slow moves to node 3.
fast moves to node 5 and then loops back to node 2.
Third Iteration:

slow moves to node 4.
fast moves to node 3 and then to node 4.
Meeting Point:
At the third iteration, both slow and fast are at node 4. This is the point where they meet, indicating that there is a cycle in the list.
'''