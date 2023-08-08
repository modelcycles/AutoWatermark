# AutoWatermark
AutoWatermark is a GUI application to automate the watermarking process for a batch of images depends on their brightness. It allows users to select JPG images, white and black watermark PNGs, and apply them automatically to the images at selected positions with the specified size ratio.

Demo video:
![Demo](./Assets/demo.gif)

## Features
* Select a folder containing JPG images to be watermarked.
* Select white and black watermark PNG files.
* Choose the watermark position from a 3x3 grid.
* Set the watermark size ratio (from 0 to 1).
* Apply watermarks to the selected images with the click of a button.

## Dependencies
* Python 3
* OpenCV (cv2)
* NumPy
* PyQt5
* PIL (Pillow)

## Installation
First, you will need to install the required dependencies. You can install them using pip:

```bash
pip install opencv-python numpy PyQt5 pillow
```

## Building the Executable (Windows)
1. **Install pyinstaller**: You can build an executable file using PyInstaller. First, make sure you have PyInstaller installed:

```bash
pip install pyinstaller
```

2. **Build the Executable**: Next, use the following command to build the `.exe` file:

```bash
pyinstaller -w -F --add-data="AutoWatermark.ui;./" AutoWatermark.py
```

3. **Locate the Executable**: After running the command, you'll find the a standalone executable named `AutoWatermark.exe` in the `dist` folder.

## Building for macOS
If you are using a macOS system, you can build the application into a standalone .app bundle using PyInstaller. The process is similar to building the Windows executable, but the command has a different format for the --add-data option.

1. **Install PyInstaller**: If you haven't installed PyInstaller, install it using:

```bash
pip install pyinstaller
```
2. **Build the Application**: Use the following command to build the .app bundle:

```bash
pyinstaller -w -F --add-data="AutoWatermark.ui:./" AutoWatermark.py
```
Note the change in the `--add-data` option, using a colon (`:`) instead of a semicolon (`;`).

3. **Locate the Application**: After running the command, you'll find the `AutoWatermark.app` bundle in the `dist` folder.

### Additional Notes for macOS
Depending on your macOS security settings, you might need to allow the application to run from unidentified developers. You can do this by going to **System Preferences > Security & Privacy > General** and clicking the **"Open Anyway"** button next to the application's name.

## How to Use
* **Select JPG images folder**: Choose a folder containing JPG images to be watermarked.
* **Select white watermark PNG**: Choose a PNG file for the white watermark.
* **Select black watermark PNG**: Choose a PNG file for the black watermark.
* **Choose Watermark Position**: Select the desired position for the watermark from the 3x3 grid.
* **Set Watermark Size Ratio**: Adjust the size ratio of the watermark (from 0 to 1).
* **Apply**: Click the "Apply!" button to apply the watermarks to the selected images.

## License
This project is open-source and available under the MIT License.

*Made by Haesung Oh*

*Contributor: Yongcheol Cho*

