import cv2, os, sys
import numpy as np
from glob import glob
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PIL import Image


def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


main_ui = resource_path("AutoWatermark.ui")
Ui_MainWindow = uic.loadUiType(main_ui)[0]


class MainWindow(QWidget, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.ratio = 0.08
        self.image_dir = ""
        self.images = []
        self.white = None
        self.black = None

        self.resize(900, 300)

        mainLayout = QVBoxLayout()

        self.text = QTextBrowser(self)
        self.text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        mainLayout.addWidget(self.text)

        buttonLayout = QHBoxLayout()

        self.button0 = QPushButton("Select JPG images folder", self)
        self.button0.clicked.connect(self.button0Clicked)
        buttonLayout.addWidget(self.button0)

        self.button1 = QPushButton("Select white watermark PNG", self)
        self.button1.clicked.connect(self.button1Clicked)
        buttonLayout.addWidget(self.button1)

        self.button2 = QPushButton("Select black watermark PNG", self)
        self.button2.clicked.connect(self.button2Clicked)
        buttonLayout.addWidget(self.button2)

        self.button3 = QPushButton("Apply!", self)
        self.button3.clicked.connect(self.button3Clicked)
        buttonLayout.addWidget(self.button3)

        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)

    def button0Clicked(self):
        fname = QFileDialog.getExistingDirectory(self, "Select Folder", "")
        self.images = glob(f"{fname}/*.jpg")
        self.images = glob(f"{fname}/*.jpeg") + self.images
        self.images = glob(f"{fname}/*.JPG") + self.images
        self.images = glob(f"{fname}/*.JPEG") + self.images
        print(self.images)
        self.text.append(f"JPG folder selected: {fname}")

    def button1Clicked(self):
        fname = QFileDialog.getOpenFileName(
            self, "Select White Watermark", "", "PNG Files (*.png)"
        )
        self.white = fname[0]
        self.text.append(f"White watermark selected: {fname[0]}")

    def button2Clicked(self):
        fname = QFileDialog.getOpenFileName(
            self, "Select Black Watermark", "", "PNG Files (*.png)"
        )
        self.black = fname[0]
        self.text.append(f"Black watermark selected: {fname[0]}")

    def button3Clicked(self):
        self.AutoWatermark(self.images, self.ratio, self.white, self.black)
        self.text.append("Applying watermarks complete!")

    def kor_imread(self, path):
        img_array = np.fromfile(path, np.uint8)
        return cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    def kor_pngread(self, path):
        img_array = np.fromfile(path, np.uint8)
        return cv2.imdecode(img_array, cv2.IMREAD_UNCHANGED)

    def AutoWatermark(self, image, ratio, white, black):
        for item in image:
            item = item.replace("\\", "/").replace("\\\\", "/")
            with open(item, "rb") as f:
                meta = Image.open(f)
            info = meta.info

            img = self.kor_imread(item)
            if img is None:
                self.text.append(f"Failed to read image: {item}")
                continue

            h_img, w_img, _ = img.shape

            dst = img[
                int(h_img - (h_img * ratio)) : h_img,
                int(w_img - (w_img * ratio)) : w_img,
            ]

            if np.mean(dst) / 255 > 0.5:
                logo = self.kor_pngread(black)
            else:
                logo = self.kor_pngread(white)

            h_logo, w_logo, _ = logo.shape

            logo = cv2.resize(
                logo,
                (int(w_img * ratio), int(w_img * ratio * h_logo / w_logo)),
                interpolation=cv2.INTER_CUBIC,
            )
            h_logo, w_logo, _ = logo.shape

            alpha = logo[:, :, 3]
            rgb = logo[:, :, :3]

            alpha = np.expand_dims(alpha, axis=2)
            alpha = np.repeat(alpha, 3, axis=2)

            destination = img[h_img - h_logo : h_img, w_img - w_logo : w_img]
            result = cv2.multiply(destination.astype(float), (1 - (alpha / 255)))
            result += cv2.multiply(rgb.astype(float), (alpha / 255))
            result = result.astype(np.uint8)

            img[h_img - h_logo : h_img, w_img - w_logo : w_img] = result

            result_image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

            with open(item, "wb") as f:
                result_image.save(f, **info)

            # extension = os.path.splitext(item)[1]

            # result, encoded_img = cv2.imencode(extension, img)

            # if result:
            #     with open(item, mode="w+b") as f:
            #         encoded_img.tofile(f)
            # else:
            #     self.text.append(f"Failed to write image: {item}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())
