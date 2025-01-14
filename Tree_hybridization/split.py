import argparse
import random


def sample(input, output1,output2, num):
    total = 0
    with open(input, 'r') as fr:
        for line in fr:
            total += 1
        if total < num:
            num = total
            print("Warning: number of examples is less than the number of samples.")
            # raise ValueError
    # get indices by mode
    indices = set(random.sample(range(total), num))
    # sample
    with open(input, 'r') as fr:
        with open(output1, 'w') as fw1:
            with open(output2, 'w') as fw2:
                for i, line in enumerate(fr):
                    if i not in indices:
                        fw2.write(line)
                    else:
                        fw1.write(line)
