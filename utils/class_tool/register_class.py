"""
# File       : register_class.py
# Time       ：2022/9/10 23:14
# Author     ：lemondyoung
# version    ：python 3
# Description：
"""

"""
使用了注册表模式和单例模式
其中单例模式的实现是通过元类来控制的
注册表模式通过魔术方法实现了一些列表操作
"""
from utils.func import get_func_info

# 单例类
class SingleClass(type):
    instance_dict = {}
    def __call__(cls):
        if cls not in cls.instance_dict:
            cls.instance_dict[cls] = super().__call__()
        return cls.instance_dict[cls]


# 注册基类(注册表模式)
class RegisterBase(dict):
    def __init__(self, *args, **kwargs):
        super(RegisterBase, self).__init__(*args, **kwargs)
        self._dict = {}

    # 注册对象字典
    def register_dict(self, dic):
        return [self.register(func, func_name) for func_name, func in dic.items()]

    # 注册的单个对象
    def register(self, func=None, func_name=None, func_info=None):
        if not func:  # 装饰器调用
            return lambda f: self.register_func(f, func_name)
        else:  # 普通调用
            return self.register_func(func, func_name)

    # 具体的注册方法
    def register_func(self, func, func_name):
        def add_register_item(key, value):
            if not callable(value):
                raise Exception(f"{value}对象任务不可调用!")
            if key in self._dict:
                print(f"warning: \033[33m{value.__name__} 对象名已经被注册！重新绑定\033[0m")
            self[key] = value
            return value
        if func_name and callable(func):  # 可调用对象并指定名称，完整的情况下
            return add_register_item(func_name, func)
        elif func and callable(func_name):  # 颠倒了（等再考虑一下会不会与其他正常情况冲突）
            return add_register_item(key=func, value=func_name)
        elif callable(func):  # 名字缺省，但对象可调用，用对象本身的名字
            return add_register_item(func.__name__, func)
        else:  # 如果不可调用，说明传入的是注册的可调用对象的名字，把它当名字传递，同时设置匿名函数（参数x代表即将被装饰调用的func对象本身）
            return lambda x: add_register_item(func, x)

    # 让类实例成为字典的决定性的两个方法
    def __setitem__(self, key, value):
        self._dict[key] = value

    def __getitem__(self, key):
        return self._dict[key]

    # 需要自己定义get方法
    def get(self, key):
        try:
            return self._dict[key]
        except KeyError:
            print('当前注册类，无%s注册信息' % key)
            return None

    def get_func_info(self, key):
        func = self.get(key)
        return get_func_info(func)

    def __contains__(self, key):
        return key in self._dict

    def __str__(self):
        return str(self._dict)

    def keys(self):
        return self._dict.keys()

    def values(self):
        return self._dict.values()

    def items(self):
        return self._dict.items()


# 数据函数注册类
class ParserRegister(RegisterBase, metaclass=SingleClass):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dict = {}


class DoubanParserRegister(ParserRegister):
    pass


class ZhihuParserRegister(ParserRegister):
    pass




if __name__ == '__main__':
    data_map = DataFunctionRegister()


    def test():
        pass
    @data_map.register(func_name='test1111')
    def test1():
        pass

    data_map.register(test)
    print(data_map)
    data_map.register(test, 'tt')
    print(data_map)

    data_map.register_dict({'t2': test, test: 't3'})
    print(data_map)