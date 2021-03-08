# -*- coding:utf-8 -*-
import random


all_chunklen = []
all_data = []
all_garbages_datas = [] #用于存放垃圾数据
All_data_remark_garb = [] #用于存放最终插入垃圾数据后的结果


def random_split(string,count):
    length = len(string)
    num = range(1, length+1)
    nums = random.sample(num, count)
    nums.sort(reverse=False)

    start_point = 0
    for i in range(count):
        chunk_len = str(nums[i]-start_point)
        print(chunk_len)
        all_chunklen.append(chunk_len)
        data = string[start_point:nums[i]]
        all_data.append(data)
        print(data)
        start_point = nums[i]

        if i == count-1:
            chunk_len = str(length - start_point)
            all_chunklen.append(chunk_len)
            print(chunk_len)
            data = string[start_point:length]
            all_data.append(data)
            print(data)
            break



def garbage_data(min_size,max_size,count):
    alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*(),./\\|{}[] :;~`'
    n = 0

    while n <= count:
        data_len = random.randint(min_size,max_size+1)
        characters = random.sample(alphabet, data_len)
        characters_toStr = ';' + ''.join(characters)
        n+=1
        garbages_data = characters_toStr
        all_garbages_datas.append(garbages_data)



def create_rs_data(count):
    for i in range(count+1):
        data = str(all_chunklen[i]) + str(all_garbages_datas[i]).strip('\n') + '\n' + str(all_data[i])
        print(data)



if __name__ == '__main__':
    string = input("输入待拆分字符串\n")
    count = int(input("输入要拆分的块数\n")) - 1
    random_split(string, count)
    choice = input("是否在注释中插入垃圾数据？(Y/N)\n")
    if choice == "Y":
        min_size = input("请输入垃圾数据的最小长度\n")
        max_size = input("请输入垃圾数据的最大长度\n")
        garbage_data(int(min_size),int(max_size),count)
        create_rs_data(count)
        input("按任意键退出...")
    elif choice == "N":
        input("按任意键退出...")


