import sys
import cv2
import pandas as pd
from PyQt5.QtWidgets import QMainWindow, QApplication, QFrame, QFileDialog
from PyQt5.uic import loadUi
import seaborn as sns
import matplotlib.pyplot as plt


class MainWindow(QMainWindow, QFrame):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("ui/main.ui", self)

        self.loadFileButton.clicked.connect(self.click)
        self.zoomButton.clicked.connect(self.zoomclick)

        self.image.setStyleSheet(f"border-image : url(image/homeimage.jpg) 0 0 0 0 stretch stretch")
        self.setWindowTitle("DATA VISUALIZATION")

        self.show()

    def zoomclick(self):
        img = cv2.imread(f"image/{self.activeText}.png")
        plt.imshow(img)
        plt.show()

    def click(self):

        filename = QFileDialog.getOpenFileName()
        print(filename)
        self.path = filename[0]
        if self.path == "":
            pass
        else:
            self.fileName.setText((self.path.split("/")[-1]).upper())
            self.df = pd.read_csv(self.path)
            self.column_item.clear()
            self.column_item.addItem("Select")
            for i in self.df.columns:
                self.column_item.addItem(i)
            self.column_item.activated[str].connect(self.onActivated)

    def onActivated(self, text):
        self.activeText = text
        if self.activeText == "Select":
            pass

        elif (self.df[text].dtype == "float64") | (self.df[text].dtype == "int64"):

            self.type.setText("TYPE : " + str(self.df[text].dtype))
            self.count.setText("COUNT : " + str(self.df.count()[text]))
            self.mean.setText("MEAN : " + str(self.df.mean()[text]))
            self.std.setText("STD : " + str(self.df.std()[text]))
            self.min.setText("MIN : " + str(self.df.min()[text]))
            self.max.setText("MAX : " + str(self.df.max()[text]))
            self.null_count.setText("NULL COUNT : " + str(self.df.isnull().sum()[text]))
            self.generateImage(0, text)


        else:
            self.type.setText("TYPE : " + str(self.df[text].dtype))
            self.count.setText("COUNT : " + str(self.df.count()[text]))
            self.mean.setText("MEAN : ")
            self.std.setText("STD : ")
            self.min.setText("MIN : ")
            self.max.setText("MAX : ")
            self.null_count.setText("NULL : " + str(self.df.isnull().sum()[text]))
            self.generateImage(1, text)

    def generateImage(self, type, text):

        if type == 0:
            sns.kdeplot(self.df[str(text)], shade=True)
            plt.savefig(f'image/{text}.png', bbox_inches="tight")
            plt.clf()
        else:
            sns.barplot(x=self.df[text].index, y=text, data=self.df)
            plt.savefig(f'image/{text}.png', bbox_inches="tight")
            plt.clf()
        self.image.setStyleSheet(f"border-image : url(image/{text}.png) 0 0 0 0 stretch stretch")


app = QApplication(sys.argv)
window = MainWindow()
app.exec_()
