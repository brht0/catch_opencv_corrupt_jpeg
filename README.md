# Catch Corrupt JPEGs (OpenCV Extraneous Bytes Warning)

There is a known issue with `cv2.imread` silently failing. The function does not throw an exception when called with corrupted JPEG images. Additionally, the warning will not be logged into `stdout` or `stderr`. This makes it impossible to pipe to another process. However, the warning is printed onto the `gnome-terminal` output, which can be logged. This repository presents a workaround solution to catch corrupt JPEGs programmatically in GNOME environments.

## Requirements

This repository utilizes the `gnome-terminal` command, so GNOME is required. With some work, this can be extended to MATE using `mate-terminal`. Pull requests are welcome.

Tested on Ubuntu 20.04.6 LTS, GNOME version 3.36.8.

## How to run

The repository includes a couple corrupt JPEG examples inside `corrupted/`. The demo script will run the checks on these images, which can be ran with: `python3 gnome_catch_std.py`. The script can be used as a reference for your applications.

## How it works

The core of this repository lies in the following command:

`
(gnome-terminal --title='session-name' -- script -f log.txt -c 'python3 read_images.py /path/to/images') && xdotool windowminimize $(xdotool search --name 'session-name'|head -1)
`

The images are read in another terminal, which will create a log file of the entire terminal output. This can then be parsed for the "Corrupt JPEG" warnings.

## Why is it so complicated?

OpenCV developers do not classify the silent JPEG error as a bug, [see the rejected Pull Request](https://github.com/opencv/opencv/pull/3314). Contrary to the developers response in the thread, `cv2.imread` does not always return an empty image when the JPEG is corrupted. However, as OpenCV is open-source, you can [fix the bug yourself](https://stackoverflow.com/questions/9131992/how-can-i-catch-corrupt-jpegs-when-loading-an-image-with-imread-in-opencv) by rebuilding OpenCV with minor modifications. This repository works without rebuilding OpenCV.

Piping the output to another stream is not possible, as the warning is not produced into `stdout` or `stderr`. This prevents any python solutions where output stream is piped to a file. Additionally, piping in the terminal does not work either (`python3 read_images.py corrupted/ > log.txt`), as the warning still is printed terminal, and not in the file.

From my testing, elegant solutions such as `PIL.verify` could not catch extraneous bytes. However, `PIL` can catch prematurely ended JPEGs. It is possible that there is some library that can validate JPEGs. In case that is true, please let me know. This was the best solution I could come up with next to optical character recognition. 

## Important Notes

- Results may vary on different systems.
- Not intended for production.

## To corrupt more images

The repository includes a program to create corrupt images. The images can be generated with `python3 create_corrupt_images.py`. This script creates a cutoff image, and a JPEG with extraneous bytes before the `0xD9` marker. These induce the uncatchable warnings in the OpenCV JPEG decoder. To test out other corrupt markers, use a reference like [https://www.disktuna.com/list-of-jpeg-markers/](https://www.disktuna.com/list-of-jpeg-markers/).

## TODO

- Demo program to verify that other solutions do not work (PIL, skimage, etc)
- Explain the commands
