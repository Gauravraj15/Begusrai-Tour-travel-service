# nums=[1,3,7,5,6,9,4,8,10]
# def Selection_sort(nums):
#     n=len(nums)
#     for i  in range(n):
#         min_ind=i
#         for j in range(i+1,n):
#             if nums[j] < nums[min_ind]:
#                 min_ind=j
#         nums[i], nums[min_ind] = nums[min_ind],nums[i]
# Selection_sort(nums)                
# print(nums)


nums=int(input("Enter any number to know fibonacci value"))
def Fibonnaci_value(nums):
    if nums==0 or nums==1:
        return nums
    return Fibonnaci_value(nums-1)+Fibonnaci_value(nums-2)

result=Fibonnaci_value(nums)
print(result)