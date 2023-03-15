
from .utils.com_utils import cvt_class2df 

class TestClass:
    def __init__(self):
        self.var1 = "hello"
        self.var2 = 123
        self.var3 = True
        self.__exclude1 = "exclude"
        self.__exclude2 = "exclude"
        
test_obj = TestClass()

# Test 1: basic usage
result_df = cvt_class2df(test_obj)
print(result_df)

# Test 2: exclude variables
result_df = cvt_class2df(test_obj, exc="^__")
print(result_df)

# Test 3: exclude variables and apply condition
result_df = cvt_class2df(test_obj, exc="^__", condition=True)
print(result_df)

