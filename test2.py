import sys

# from data_parse.parse_tools.danmaku2ass import main
# sys.argv = ['file', r'D:\video\为了逃避生活，我骑行流浪一年了，每天都在向着远方前行，但是最近也迷茫了.cmt.xml',
#             '-o', r'D:\video\为了逃避生活，我骑行流浪一年了，每天都在向着远方前行，但是最近也迷茫了.cmt.ass',
#             '--size', '1920x1080', '--font', '"MS PGothic"', '--fontsize', '44', '--alpha', '0.7', '-dm', '15', '-ds', '5']
# main()
#
d = {'a': 1, 'b': 1, 'c': 3, }
key1 = list(d.keys())[0]
value1 = d.pop(key1)
print({key1: value1})
print(d)
