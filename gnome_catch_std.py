import subprocess
import time
import os

def check_if_session_alive(session_title):
    cmd = f"xdotool search --name '{session_title}'|head -1"
    result = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
    return len(result.stdout)

def catch_corrupt_jpeg_without_rebuilding_opencv(path_to_images, *, log_file, read_script="read_images.py", session_title="anything-is-fine"):
    cmd = f"(gnome-terminal --title='{session_title}' -- script -f {log_file} -c 'python3 {read_script} {path_to_images}') && xdotool windowminimize $(xdotool search --name '{session_title}'|head -1)"
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    while check_if_session_alive(session_title):
        time.sleep(0.1)
    with open(log_file, "r") as f:
        terminal_output = f.read()
    corrupted_jpegs = []
    prev_jpeg = ""
    lines = terminal_output.split("\n")
    for line in lines[lines.index("[START]")+1:lines.index("[END]")]:
        if line.startswith(f"[{read_script}]"):
            prev_jpeg = line[len(f"[{read_script}]")+1:]
        else:
            print(f"Found corrupt image {prev_jpeg}, with error: \"{line}\".")
            corrupted_jpegs.append(prev_jpeg)
    return corrupted_jpegs

if __name__ == '__main__':
    path_to_images = "corrupted"
    output_path = "output"
    corrupted_list = os.path.join(output_path, "corrupted_images.txt")
    read_script = "read_images.py"

    if not os.path.exists(output_path):
        os.makedirs(output_path)
    corrupted_jpegs = catch_corrupt_jpeg_without_rebuilding_opencv(path_to_images, session_title="this-is-a-test", log_file=os.path.join(output_path, "test.log"))
    with open(corrupted_list, "w") as f:
        for jpeg in corrupted_jpegs:
            f.write(f"{jpeg}\n")
    print(f"Found {len(corrupted_jpegs)} corrupted JPEG(s) in {path_to_images}. The corrupted images are: {corrupted_jpegs}")
    print(f"Results can be found in {corrupted_list}.")
