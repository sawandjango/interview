# Find the square root using the binary search 
# input = 4 
# output = 2
class Test:
    def __init__(self):
        pass
    def squre_root(low, high,num):
        mid = (low + high)//2
        while low <=high:
            if mid * mid == num: # 2 *2 = 4 input
                return mid
            elif mid * mid < num:
                mid = mid +1
            elif mid * mid > num:
                mid = mid =1 

num = 4 
obj = Test()
low = 0
high = num 
result = obj.squre_root(low, high,num)    
print(result)


#mid * mid < num 
 
