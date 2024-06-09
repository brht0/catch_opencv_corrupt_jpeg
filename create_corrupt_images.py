#!/bin/python3
import os
import cv2
import random
import time

def create_corrupt_extraneous(uncorrupted_file, output_corrupted_file):
    with open(uncorrupted_file, "rb") as fr:
        contents = bytearray(fr.read())
        idx = contents.find(bytearray([0xFF, 0xD9]))
        for i in range(100):
            contents[idx - 1 - i] = 0x12
        with open(output_corrupted_file, "wb") as fw:
            fw.write(contents)

def create_corrupt_premature(uncorrupted_file, output_corrupted_file):
    with open(uncorrupted_file, "rb") as fr:
        contents = bytearray(fr.read())
        with open(output_corrupted_file, "wb") as fw:
            fw.write(contents[:2*len(contents)//3])

if __name__ == '__main__':
    random.seed(time.time())
    output_folder = "corrupted"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    create_corrupt_extraneous("images/corrupt.jpg", f"{output_folder}/corrupt.jpg")
    create_corrupt_premature("images/cut.jpg", f"{output_folder}/cut.jpg")

    print("Extraneous bytes:")
    cv2.imread(f"{output_folder}/corrupt.jpg")

    print("\nPremature end:")
    cv2.imread(f"{output_folder}/cut.jpg")

    print("\nNon-corrupt does not give any errors.")
    cv2.imread(f"images/good.jpg")
