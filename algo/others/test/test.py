'''
input = ['1','2','4','6']
fist_pointer = 0
last_pointer = len(input) -1 #3
'''
counter_as_index = 0
class Test:
    def __init__(self, ):
        pass
   
    def travese(self, input):        
        fist_pointer = 0
        last_pointer = len(input) -1
        fist_pointer = fist_pointer + counter_as_index 
        if fist_pointer < last_pointer: # 0 < 3
            print(input[fist_pointer])
            counter_as_index +=1
            self.travese(input) # recursivly            
            

input = ['1','2','4','6']
obj = Test()    
obj.travese(input)