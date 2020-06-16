### LƯU Ý: ĐÂY LÀ MỘT THƯ VIỆN TỰ TẠO CỦA EM VỀ CÁC HÀM TIỆN ÍCH TRONG PYTHON
### Link Github: https://github.com/huykingsofm/PyUtils/blob/master/Utils.py
### ĐỐI VỚI BÀI NÀY, thầy chỉ cần xem xét 2 chỗ
### * Hàm get_file_size() : Trả về kích thước file
### * Lớp Generate_Writable_Path : Trả về một đường dẫn để ghi với quyền người dùng hiện tại


version = "1.2"
from random import randint
import random
from math import sqrt
import os
import timeit
import sys

def get_bit(a, n):
    return (a >> n) & 1

def turn_on_bit(a, n):
    return (1 << n) | a

def turn_off_bit(a, n):
    return a & ~(1 << n)

def get_file_size(fn):
    size = os.stat(fn).st_size
    return size

def array_multiply(arr: list, multiplier: float, shuffle= True, shuffle_last= True):
    if len(arr) == 0:
        return arr
        
    integer = int(multiplier)
    resident = multiplier - integer
    
    last = arr.copy()
    if shuffle_last:
        random.shuffle(last)
    
    new_arr = []
    for _ in range(integer):
        t = arr.copy()
        if shuffle:
            random.seed(int(timeit.timeit() * 1e10))
            random.shuffle(t)
        new_arr.extend(t)
    
    last_len = int(resident * len(arr))
    new_arr.extend(last[:last_len])
    return new_arr

def get_name_in_path(path:str):
    path = path.rstrip("/").rstrip("\\")
    path = path.replace("\\", "/")
    return path.split("/")[-1]

def GetScreenSize():
    import wx
    _ = wx.App(False)
    return wx.GetDisplaySize()

def GetCurrentWorkingDir():
    return os.getcwd()

def permutation(N):
    perm = list(range(N))
    random.shuffle(perm)
    return perm

def squarize(inp):
    if  sqrt(len(inp)) != int(sqrt(len(inp))):
        raise Exception("input len ({}) can not conver to square matrix".format(len(inp)))
    
    square = []
    N = int(sqrt(len(inp)))
    for i in range(N):
        square.append([])
        for j in range(N):
            square[i].append(inp[i * N + j])
            
    return square
     

def flatten(inp):
    return __flatten__(inp, [])
    
def __flatten__(inp, out : list):
    if type(inp) != type([]):
        out.append(inp)
        return out
    
    for element in inp:
        __flatten__(element, out)
    return out

class Generate_Writable_Path:
    list_disk_name_prior = ['c', 'd', 'e']
    list_disk_name = ['f', 'g', 'h', 'i', 'j', 'k']
    list_disk_name_prior.extend(list_disk_name)
    avoid = ["$RECYCLE.BIN", "$Recycle.Bin"]
    
    @staticmethod
    def __gen__(path):
        try:
            all_files = os.listdir(path)
            oder = permutation(len(all_files))

            for i in oder:
                if os.path.isdir(path + all_files[i]) and all_files[i] not in Generate_Writable_Path.avoid:
                    res = Generate_Writable_Path.__gen__(path + all_files[i] + "/")
                    if res is not False:
                        return res
                        
            # if no-exist-dir
            return path
        except:
            return False
    
    @staticmethod
    def gen():
        for disk in Generate_Writable_Path.list_disk_name_prior:
            ret = Generate_Writable_Path.__gen__(disk + "://")
            if ret is not False:
                try:
                    with open(ret + "3131879187291.temp", "wb"):
                        pass
                    os.remove(ret + "3131879187291.temp")
                    return ret
                except:
                    pass

if __name__ == "__main__":
    print(Generate_Writable_Path.gen())