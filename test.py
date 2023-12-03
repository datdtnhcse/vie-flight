# import os

# data_path = "/Users/guest/Desktop/NLP_HCMUT/vie-flight/Output_flight/"

# list_dir = [f"output_{ele}.txt" for ele in range(1,11)]

# for ele in list_dir:
#     with open(os.path.join(data_path, ele), 'w') as fp:
#         pass

# print(os.listdir(data_path))



# -*- coding: utf-8 -*-
from underthesea import pos_tag
print(pos_tag('Máy bay nào bay từ Đà Nẵng đến Hồ Chí Minh mất một giờ'))