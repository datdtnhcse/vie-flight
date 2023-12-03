import os

data_path = "/Users/guest/Desktop/NLP_HCMUT/vie-flight/Output_flight/"

list_dir = [f"output_{ele}.txt" for ele in range(1,11)]

for ele in list_dir:
    with open(os.path.join(data_path, ele), 'w') as fp:
        pass

print(os.listdir(data_path))