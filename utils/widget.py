



# 多种方式随机生成字符串
import random
import string
import time
import uuid


src_digits = string.digits  #string_数字
src_uppercase = string.ascii_uppercase  #string_大写字母
src_lowercase = string.ascii_lowercase  #string_小写字母
def random_password(count, type='time'):
    if type == 'digital_alp':
        # 随机生成数字、大写字母、小写字母的组成个数（可根据实际需要进行更改）
        digits_num = random.randint(1,6)
        uppercase_num = random.randint(1,8-digits_num-1)
        lowercase_num = 8 - (digits_num + uppercase_num)
        # 生成字符串
        password = random.sample(src_digits, digits_num) + random.sample(src_uppercase, uppercase_num) + random.sample(src_lowercase, lowercase_num)
        # 打乱字符串
        random.shuffle(password)
        # 列表转字符串
        new_password = ''.join(password)
    elif type == 'digital':
        new_password = str(random.randint(0, 9*count**(count-1))).zfill(8)
    elif type == 'time':
        new_password = str(int(round(time.time() * 1000)))
        if count < 10:
            new_password = new_password[0:10]
        elif count in range(10, 13):
            new_password = new_password[0:count]
        else:
            new_password = new_password
    elif type == 'uuid':
        new_password = str(uuid.uuid1()).replace('-', '')[1:count]
    return new_password


if __name__ == '__main__':
    d = random_password(count=28, type='uuid')
    print(d)