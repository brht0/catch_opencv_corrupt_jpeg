import sys
import os
import cv2

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"[{sys.argv[0]}]\n\tPlease run with path: '{sys.argv[0]} \"/path/to/images/\"'")
        exit()
    path_to_images = sys.argv[1]
    if not os.path.exists(path_to_images):
        print(f"[{sys.argv[0]}]\n\tDirectory '{path_to_images}' does not exist.")
        exit()
    images = [os.path.join(path_to_images, img) for img in os.listdir(path_to_images)]
    print("[START]")
    for path in images:
        print(f"[{sys.argv[0]}] {path}")
        cv2.imread(path)
    print("[END]")
