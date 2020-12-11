import sys
import pandas as pd

from PyQt5 import QtWidgets
from PyQt5.QtCore import QAbstractTableModel, Qt

import filtre

class filtreleme(filtre.Ui_MainWindow):
    data = None
    sure_data = None
    raitings = {'G' : 'Genel İzleyici',
     'NC-17' : '+17',
     'NR' : 'Henüz Derecelendirilmemiş İçerik',
     'PG' : 'Ebeveyn Rehberli İçerik',
     'PG-13' : '+13',
     'R' : '17 Yaşından Küçükler İçin Ebeveyn Rehberli İçerik ',
     'TV-14' : '+14',
     'TV-G' : 'Her Yaş Çocuk İçin',
     'TV-MA' : '+17 Genç İçerik',
     'TV-PG' : 'Ebeveyn Rehberli İçerik',
     'TV-Y' : '2-6 Yaş İçin',
     'TV-Y7' : '7 ve Üstü Yaş İçin',
     'TV-Y7-FV' : '7 Yaş Üstü İçin (Şiddet İçerir)',
     'UR' : 'Derecelendirilmemiş İçerik'}

    def __init__(self):
        self.netflixDataAl()
        sure_pd = self.data[['duration']]
        self.data['int_duration'] = ((sure_pd[sure_pd['duration'].str.contains(' min')])['duration'].str.replace(' min', '', regex=True)).astype(int)
        self.data['text_codes'] = self.data['rating'].map(self.raitings)


    def ekraniGoster(self):
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        self.setupUi(MainWindow)
        self.ara.clicked.connect(self.araTikla)
        self.rating.addItem('Seçiniz')
        self.rating.addItems(self.ratingData())
        self.ulke.addItem('Seçiniz')
        self.ulke.addItems(self.ulkeData())
        self.sure.setRange(0, self.data['int_duration'].max())
        self.sureYaziLabel.setText(self.sure.value().__str__())
        self.sure.valueChanged.connect(self.sureYazdir)
        MainWindow.show()
        sys.exit(app.exec_())

    def sureYazdir(self):
        self.sureYaziLabel.setText(self.sure.value().__str__())

    def araTikla(self):
        kopyaData = self.data
        if len(self.yonetmen.text()) > 0:
            kopyaData = kopyaData[kopyaData['director'].str.contains(self.yonetmen.text(),na=False, case=False)]

        if self.rating.currentText() != 'Seçiniz':
            kopyaData = kopyaData[kopyaData['text_codes'] == self.rating.currentText()]

        if self.ulke.currentText() != 'Seçiniz' :
            kopyaData = kopyaData[kopyaData['country'].str.contains(self.ulke.currentText(),na=False, case=False)]

        if self.sure.value() > 0:
            kopyaData = kopyaData[kopyaData['int_duration'].between(self.sure.value() -10, self.sure.value()+10)]

        model = pandasModel(kopyaData)
        self.sonuclar.setModel(model)

    def tekilData(self, kolon):
        kopyaData = self.data[[kolon]]
        bosOlmayan=kopyaData.dropna().reset_index()
        bosOlmayan[kolon] = bosOlmayan[kolon].str.split(",", n = 1, expand = True)
        return (bosOlmayan.sort_values(by=kolon))[kolon].unique()

    def ratingData(self):
        return self.tekilData('text_codes')

    def ulkeData(self):
        return self.tekilData('country')

    def netflixDataAl(self):
        self.data = pd.read_csv('netflix_titles.csv')


class pandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None