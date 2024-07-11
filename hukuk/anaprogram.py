# -*- coding: utf-8 -*-
"""
Created on Thu May 23 01:53:23 2024

@author: ispar
"""


#kütüphane içe aktarma
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox,QTableWidgetItem , QDialog

#Harici modüllerin içe aktarılması
from widgets import Ui_mw_Hukuk1
from Hakkinda import Ui_hakkinda
from sifreleme import Ui_sifreleme
import sqlite3

        
        
class Ui_sifreleme_class(QtWidgets.QMainWindow): ## QMainWindow sınıfından türetilen Ui_sifreleme_class adlı sınıf tanımlanır.
    def __init__(self):
        super().__init__()
        self.ui = Ui_sifreleme() # Ui_sifreleme sınıfının bir örneği oluşturulur ve self.ui değişkenine atanır.
        self.ui.setupUi(self)
        self.ui.btn_cancel.clicked.connect(self.close) # "Cancel" butonuna tıklanınca pencerenin kapanması sağlanır.
        self.ui.btn_ok.clicked.connect(self.check_password) # "OK" butonuna tıklanınca check_password metodunun çağrılması sağlanır.
        
    def check_password(self): # sifrenin dogrulugunu kontrol eden metod.
        password = self.ui.lne_sifregir.text()
        if password == "hukuk123":  # Girilen sifrenin "hukuk123" olup olmadigi kontrol edilir.
        #sifre bilgilendirme mesajlari
            QMessageBox.information(self,"Başarılı","Şifre Doğru, Programa girebilirsiniz!")
            self.anaprogramı_ac()
        else:
            QMessageBox.warning(self,"Şifre Hatalı","Şifre Hatalı, tekrar deneyiniz!")
            
    def anaprogramı_ac(self): #sınıf içindeki bir metodu tanımlar
        self.programi_ac = MainWindow()
        self.programi_ac.show()
        self.close()
        
    

class MainWindow(QtWidgets.QMainWindow, Ui_mw_Hukuk1): # Ana pencere sınıfı
    global conn  # Veritabanı bağlantısı için global değişken
    global curs  # Veritabanı kursörü için global değişken
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.baglanti_olustur() # Veritabanı bağlantısını oluştur
        self.listele()  # Veritabanındaki kayıtları listele
        
        # Buton tıklama olaylarını UI bileşenlerine bağlama
        self.btn_KayitEkle.clicked.connect(self.kayit_ekle)
        self.btn_KayitEkle.clicked.connect(self.listele)
        self.btn_Listele.clicked.connect(self.listele)
        self.btn_KayitGuncelle.clicked.connect(self.kayit_guncelle)
        self.tblw_Liste.itemSelectionChanged.connect(self.doldur)
        self.btn_KayitAra.clicked.connect(self.kayit_ara)
        self.btn_KayitSil.clicked.connect(self.kayit_sil)
        self.btn_Cikis.clicked.connect(self.cikis)
        self.btn_hakkinda.clicked.connect(self.hakkinda_goster)
       
    def veri_giris_kontrol(self,_MuvekkilAdSoyad, _DavaAvukati, _DavaliAdSoyad, \
                           _KarsiAvukat, _MuvekkilTCNo, _MuvekkilCepNo, _DavaliCepNo):
        
        # Tüm boşlukları kaldırıp sadece harflerden oluşup oluşmadığını kontrol eder
        if not _MuvekkilAdSoyad.replace(" ", "").isalpha(): 
            QMessageBox.warning(
                self,"UYARI" , "Müvekkil ad soyad yalnızca harf içermelidir" )
            return False
        
        if not _DavaAvukati.replace(" ", "").isalpha():
            QMessageBox.warning(
                self,"UYARI" , "Dava avukatı yalnızca harf içermelidir" )  # Uyarı mesajı gösterir
            return False # Kontrol başarısız olduğunda False döner
        
        if not _DavaliAdSoyad.replace(" ", "").isalpha():
            QMessageBox.warning(
                self,"UYARI" , "Davalı ad soyad yalnızca harf içermelidir" )
            return False
        
        if not _KarsiAvukat.replace(" ", "").isalpha():
            QMessageBox.warning(
                self,"UYARI" , "Karşı avukat yalnızca harf içermelidir" )
            return False
        
        # Tüm boşlukları kaldırıp sadece rakamlardan oluşup oluşmadığını kontrol eder
        if not _MuvekkilTCNo.replace(" ","").isdigit():
            QMessageBox.warning(
                self,"UYARI" , "TC no  yalnızca rakam içermelidir" )
            return False
        
        if not _MuvekkilCepNo.replace(" ","").isdigit():
            QMessageBox.warning(
                self,"UYARI" ,"Müvekkil cep no  yalnızca rakam içermelidir" )
            return False
        
        if not _DavaliCepNo.replace(" ","").isdigit():
            QMessageBox.warning(
                self,"UYARI" , "Davalı cep no  yalnızca rakam içermelidir" )
            return False
            
        
        return True
    
    # Yeni kayıt eklemek için kullanılan metod
    def kayit_ekle(self):
        
        # Kullanıcı arayüzünden alınan veriler
        _MuvekkilAdSoyad=self.lne_MuvekkilAdSoyad.text()
        _DavaAvukati=self.lne_DavaAvukati.text()
        _DavaliAdSoyad=self.lne_DavaliAdSoyad.text()
        _KarsiAvukat=self.lne_KarsiAvukat.text()
        _MuvekkilTCNo=self.lne_MuvekkilTCNo.text()
        _MuvekkilCepNo=self.lne_MuvekilCepNo.text()
        _DavaliCepNo=self.lne_DavaliCepNo.text()
        
        # Medeni durumu kontrolü
        if self.rbtn_Bekar.isChecked():
            _MedeniDurumu="Bekar"
        elif self.rbtn_Evli.isChecked():
            _MedeniDurumu="Evli"
        
        # Uzlaşma durumu kontrolü  
        if self.rbtn_Var.isChecked():
            _Uzlasma="Var"
        elif self.rbtn_Yok.isChecked():
            _Uzlasma="Yok"
       
        
        
        if not self.veri_giris_kontrol(_MuvekkilAdSoyad, _DavaAvukati, _DavaliAdSoyad, _KarsiAvukat, _MuvekkilTCNo, _MuvekkilCepNo, _DavaliCepNo):
            return # Eğer veri giriş kontrolü başarısız olursa, fonksiyondan çık
        
        _Ilce=self.cmb_ilce.currentText()
        _MuvekkilAdresi=self.txt_MuvekkilAdresi.toPlainText()
        _Ucret=self.spnb_ucret.value()
        _DavaliAdresi=self.txt_DavaliAdresi.toPlainText()
        _DavaTuru=self.cmb_DavaTuru.currentText()
        _MahkemeBinasi=self.cmb_MahkemeBinasi.currentText()
        _DurusmaSalonu=self.cmb_DurusmaSalonu.currentText()
        _DurusmaTarihi=self.clw_DurusmaTarihi.selectedDate().toString("dd-MM-yyyy")
        
        #Veri tabanı işlemleri
        try:
            # SQL sorgusu ile veri ekleme
            self.curs.execute("INSERT INTO buro \
                          (MuvekkilAdSoyad, DavaAvukati, DavaliAdSoyad, KarsiAvukat, MuvekkilTCNo, MuvekkilCepNo, DavaliCepNo ,\
                           MedeniDurumu, Ilce, MuvekkilAdresi, Ucret, DavaliAdresi, DavaTuru, Uzlasma, \
                              MahkemeBinasi, DurusmaSalonu, DurusmaTarihi)" 
                              "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",  \
                              (_MuvekkilAdSoyad, _DavaAvukati, _DavaliAdSoyad, _KarsiAvukat, _MuvekkilTCNo, _MuvekkilCepNo, \
                                   _DavaliCepNo, _MedeniDurumu, _Ilce, _MuvekkilAdresi, _Ucret, _DavaliAdresi, \
                                       _DavaTuru, _Uzlasma, _MahkemeBinasi, _DurusmaSalonu, _DurusmaTarihi))
            
            self.conn.commit() # Veritabanı işlemlerini kaydet

            QMessageBox().information(self,"BİLGİ","Kayıt başarıyla eklendi.")
            
        except sqlite3.Error as e:
            QMessageBox().critical(self,"Hata","Kayıt eklenirken hata: " +str(e))
    
    # Veritabanı bağlantısını oluşturmak için kullanılan metod        
    def baglanti_olustur(self):
        try:
            self.conn=sqlite3.connect("veritabani.db") # Veritabanına bağlantı oluştur
            self.curs=self.conn.cursor() # Veritabanı üzerinde işlem yapmak için bir cursor oluştur
            self.sorguCreTblburo = ("CREATE TABLE IF NOT EXISTS buro("  # 'buro' tablosunu oluşturma sorgusu                                                               \
                                    "Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, " # Otomatik artan birincil anahtar sütunu                                                  \
                                       #yazılan bilgilerin sutünü boş olmaz
                                       "MuvekkilAdSoyad TEXT NOT NULL UNIQUE, "                                                            \
                                       "DavaAvukati TEXT NOT NULL, "                                                                        \
                                       "DavaliAdSoyad TEXT NOT NULL, "                                                                       \
                                       "KarsiAvukat TEXT NOT NULL, "                                                                           \
                                       "MuvekkilTCNo TEXT NOT NULL, "                                                                           \
                                       "MuvekkilCepNo TEXT NOT NULL, "                                                                           \
                                       "DavaliCepNo TEXT NOT NULL, "                                                                              \
                                       "MedeniDurumu TEXT NOT NULL, "                                                                              \
                                       "Ilce TEXT NOT NULL, "                                                                                       \
                                       "MuvekkilAdresi TEXT NOT NULL, "                                                                           \
                                       "ucret REAL NOT NULL, "                                                                                        \
                                       "DavaliAdresi TEXT NOT NULL, "                                                                            \
                                       "DavaTuru TEXT NOT NULL, "                                                                                       \
                                       "Uzlasma TEXT NOT NULL, "                                                                                     \
                                       "MahkemeBinasi TEXT NOT NULL, "                                                                                    \
                                       "DurusmaSalonu TEXT NOT NULL, "                                                                                     \
                                       "DurusmaTarihi TEXT NOT NULL) "
                                       )
            self.curs.execute(self.sorguCreTblburo) # Tabloyu oluşturma sorgusunu çalıştır
            self.conn.commit() # Yapılan değişiklikleri veritabanına kaydet
        except sqlite3.Error as e:
            print("SQlite veritabanı hatası:", e) # Hata mesajı yazdır
            
    # Veritabanındaki kayıtları listelemek için kullanılan metod
    def listele(self):
        try:
            self.tblw_Liste.clear()  # Tabloyu temizler
            
            # Tablonun başlıklarını ayarlar
            self.tblw_Liste.setHorizontalHeaderLabels(('NO','Müvekkil Ad Soyad','Dava Avukatı','Davalı Ad Soyad',\
                                                       'Karşı Avukat','Müvekkil TC No','Müvekkil Cep No','Davalı Cep No',\
                                                       'Medeni Durumu','İlçe','Müvekkil Adresi','Ücret','Davalı Adresi',\
                                                       'Dava Türü','Uzlaşma','Mahkeme Binası','Duruşma Salonu','Duruşma Tarihi'))

            self.tblw_Liste.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch) # Başlıkları tablo genişliğine göre ayarlar
            
            self.curs.execute("SELECT * FROM buro") # 'buro' tablosundaki tüm kayıtları alır
            for satirIndex, satirVeri in enumerate(self.curs):  # Her bir satır için
                self.tblw_Liste.insertRow(satirIndex) # Yeni bir satır ekler
                for sutunIndex, sutunVeri in enumerate(satirVeri):  # Her bir sütun için
                    self.tblw_Liste.setItem(satirIndex, sutunIndex, QtWidgets.QTableWidgetItem(str(sutunVeri))) # Hücreye veriyi ekler
                
        
            #giriş elemanlarını temizler
            self.lne_MuvekkilAdSoyad.clear()
            self.lne_DavaAvukati.clear()
            self.lne_DavaliAdSoyad.clear()
            self.lne_KarsiAvukat.clear()
            self.lne_MuvekkilTCNo.clear()
            self.lne_MuvekilCepNo.clear()
            self.lne_DavaliCepNo.clear()
            self.rbtn_Bekar.setChecked(False)
            self.rbtn_Evli.setChecked(False)
            self.cmb_ilce.setCurrentIndex(-1)
            self.txt_MuvekkilAdresi.clear()
            self.spnb_ucret.setValue(8000)
            self.txt_DavaliAdresi.clear()
            self.cmb_DavaTuru.setCurrentIndex(-1)
            self.rbtn_Var.setChecked(False)
            self.rbtn_Yok.setChecked(False)
            self.cmb_MahkemeBinasi.setCurrentIndex(-1)
            self.cmb_DurusmaSalonu.setCurrentIndex(-1)
            self.clw_DurusmaTarihi.setSelectedDate(QtCore.QDate().currentDate()) # Duruşma tarihi takvimini günün tarihine ayarlar
            
        except sqlite3.Error as e:
                print("SQLite hatası:",e)
                
    # Mevcut kaydı güncellemek için kullanılan metod
    def kayit_guncelle(self):
        
        # Kullanıcıya güncelleme isteyip istemediğini sormak için bir iletişim kutusu gösterir
        cevap = QtWidgets.QMessageBox().question(self,"GÜNCELLE","Güncellemek istiyor musunuz?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox().No)
        if cevap == QtWidgets.QMessageBox().Yes:
            try:
                secili = self.tblw_Liste.selectedItems() # Tabloda seçilen öğeleri alır
                if secili: # Eğer bir öğe seçilmişse
                    _Id = int(secili[0].text()) # Seçilen satırın ID'sini alır
                    _MuvekkilAdSoyad=self.lne_MuvekkilAdSoyad.text()
                    _DavaAvukati=self.lne_DavaAvukati.text()
                    _DavaliAdSoyad=self.lne_DavaliAdSoyad.text()
                    _KarsiAvukat=self.lne_KarsiAvukat.text()
                    _MuvekkilTCNo=self.lne_MuvekkilTCNo.text()
                    _MuvekkilCepNo=self.lne_MuvekilCepNo.text()
                    _DavaliCepNo=self.lne_DavaliCepNo.text()
                    _Ilce=self.cmb_ilce.currentText()
                    _MuvekkilAdresi=self.txt_MuvekkilAdresi.toPlainText()
                    _Ucret=self.spnb_ucret.value()
                    _DavaliAdresi=self.txt_DavaliAdresi.toPlainText()
                    _DavaTuru=self.cmb_DavaTuru.currentText()
                    _Uzlasma=self.rbtn_Var.isChecked()
                    _Uzlasma=self.rbtn_Yok.isChecked()
                    _MahkemeBinasi=self.cmb_MahkemeBinasi.currentText()
                    _DurusmaSalonu=self.cmb_DurusmaSalonu.currentText()
                    _DurusmaTarihi=self.clw_DurusmaTarihi.selectedDate().toString("dd-MM-yyyy")
                    
                    if self.rbtn_Bekar.isChecked(): # Eğer bekar radio düğmesi seçiliyse
                        _MedeniDurumu="Bekar"  # Medeni durumu bekar olarak ayarlar
                    elif self.rbtn_Evli.isChecked():  # Eğer evli radio düğmesi seçiliyse
                        _MedeniDurumu="Evli" # Medeni durumu evli olarak ayarlar
                        
                    if self.rbtn_Var.isChecked(): # Eğer uzlaşma var radio düğmesi seçiliyse
                        _Uzlasma="Var" # Uzlaşmayı var olarak ayarlar
                    elif self.rbtn_Yok.isChecked():  # Eğer uzlaşma yok radio düğmesi seçiliyse
                        _Uzlasma="Yok" 
                    
                    self.curs.execute("UPDATE buro SET MuvekkilAdSoyad=?, DavaAvukati=?, DavaliAdSoyad=?, \
                                      KarsiAvukat=?, MuvekkilTCNo=?, MuvekkilCepNo=?, DavaliCepNo=? ,MedeniDurumu=?, Ilce=?, \
                                      MuvekkilAdresi=?, Ucret=?, DavaliAdresi=?, DavaTuru=?, Uzlasma=?, MahkemeBinasi=?, \
                                      DurusmaSalonu=?, DurusmaTarihi=? WHERE Id=?",  \
                                        (_MuvekkilAdSoyad, _DavaAvukati, _DavaliAdSoyad, _KarsiAvukat, _MuvekkilTCNo, _MuvekkilCepNo, \
                                             _DavaliCepNo, _MedeniDurumu, _Ilce, _MuvekkilAdresi, _Ucret, _DavaliAdresi, \
                                                 _DavaTuru, _Uzlasma, _MahkemeBinasi, _DurusmaSalonu, _DurusmaTarihi, _Id)) # Değişiklikleri yapar
                        
                    self.conn.commit() # Yapılan değişiklikleri veritabanına kaydeder
                    self.listele() # Güncellenmiş verilerle tabloyu yeniden doldurur
                    
                    #Durum çubuğuna mesaj gönderir
                    self.statusbar.showMessage("Kayit Guncellendi.",10000)
                else:
                    self.statusbar.showMessage("Kaydi secin.",10000)
            except sqlite3.Error  as hata:
                self.statusbar.showMessage("Hata Olustu: " + str(hata))
        else:
            self.statusbar.showMessage("Guncelleme islemi iptal edildi.",10000)
            
    
    # Tablo seçimi değiştiğinde seçili kaydı doldurmak için kullanılan metod
    def doldur(self):
        secili = self.tblw_Liste.selectedItems()  # Tabloda seçili öğeleri alır
        if len(secili) > 0:  # Eğer bir öğe seçilmişse
        
            # Seçilen satırdaki verileri ilgili giriş kutularına yerleştirir
            self.lne_MuvekkilAdSoyad.setText(secili[1].text())
            self.lne_DavaAvukati.setText(secili[2].text())
            self.lne_DavaliAdSoyad.setText(secili[3].text())
            self.lne_KarsiAvukat.setText(secili[4].text())
            self.lne_MuvekkilTCNo.setText(secili[5].text())
            self.lne_MuvekilCepNo.setText(secili[6].text())
            self.lne_DavaliCepNo.setText(secili[7].text())
            
            #Medeni durumu ve uzlaşma durumu radyo düğmelerini ve kombobox'u ayarlar
            medenidurum = secili[8].text()
            self.rbtn_Bekar.setChecked(medenidurum == "Bekar")
            self.rbtn_Evli.setChecked(medenidurum == "Evli") 
            self.cmb_ilce.setCurrentText(secili[9].text())
            # Metin alanlarını ve diğer giriş kutularını ayarlar
            self.txt_MuvekkilAdresi.setPlainText(secili[10].text())
            self.spnb_ucret.setValue(int(secili[11].text()))
            self.txt_DavaliAdresi.setPlainText(secili[12].text())
            self.cmb_DavaTuru.setCurrentText(secili[13].text())
            uzlasmadurumu = secili[14].text()
            self.rbtn_Var.setChecked(uzlasmadurumu == "Var")
            self.rbtn_Yok.setChecked(uzlasmadurumu == "Yok")
            self.cmb_MahkemeBinasi.setCurrentText(secili[15].text())
            self.cmb_DurusmaSalonu.setCurrentText(secili[16].text())
            # Duruşma Tarihi bilgisini doldurma
            date_text = secili[17].text()
            date = QtCore.QDate.fromString(date_text,"dd-MM-yyyy") # Tarihi çözümleyerek QDate nesnesi oluşturur
            self.clw_DurusmaTarihi.setSelectedDate(date) # Duruşma tarihini ayarlar
            
        else:
            #giriş elemanlarını temizler
            self.lne_MuvekkilAdSoyad.clear()
            self.lne_DavaAvukati.clear()
            self.lne_DavaliAdSoyad.clear()
            self.lne_KarsiAvukat.clear()
            self.lne_MuvekkilTCNo.clear()
            self.lne_MuvekilCepNo.clear()
            self.lne_DavaliCepNo.clear()
            self.rbtn_Bekar.setChecked(False)
            self.rbtn_Evli.setChecked(False)
            self.cmb_ilce.setCurrentIndex(-1)
            self.txt_MuvekkilAdresi.clear()
            self.spnb_ucret.setValue(8000)
            self.txt_DavaliAdresi.clear()
            self.cmb_DavaTuru.setCurrentIndex(-1)
            self.rbtn_Var.setChecked(False)
            self.rbtn_Yok.setChecked(False)
            self.cmb_MahkemeBinasi.setCurrentIndex(-1)
            self.cmb_DurusmaSalonu.setCurrentIndex(-1)
            self.clw_DurusmaTarihi.setSelectedDate(QtCore.QDate().currentDate()) # Duruşma tarihini güncel tarih olarak ayarlar
            if date.isValid(): # Eğer seçilen bir tarih varsa
                self.clw_DurusmaTarihi.setSelectedDate(date)  # Seçilen tarihi ayarlar
            else:
                self.clw_DurusmaTarihi.setSelectedDate(QtCore.QDate.currentDate())  # Duruşma tarihini güncel tarih olarak ayarlar  
            
    
    # Kayıt aramak için kullanılan metod        
    def kayit_ara(self):
        
        # Aranacak değerleri alır
        aranan1 = self.lne_MuvekkilTCNo.text()
        aranan2 = self.lne_MuvekilCepNo.text()
        aranan3 = self.lne_DavaliCepNo.text()
        
        # Filtreleme için kullanılacak koşulları tutacak bir liste oluşturur
        filtre = []
        if aranan1:
            filtre.append("MuvekkilTCNo=?")
        if aranan2:
            filtre.append("MuvekkilCepNo=?")
        if aranan3:
            filtre.append("DavaliCepNo=?")
            
        filtre_sorgusu = "OR ".join(filtre)
         
        if filtre_sorgusu:
            # Sorguyu ve parametreleri hazırlar
            sorgu = "SELECT * from buro WHERE " + filtre_sorgusu
            parametreler = tuple(filter(lambda x: x,[aranan1, aranan2, aranan3]))
             
            # Sorguyu çalıştırır ve sonuçları alır
            self.curs.execute(sorgu, parametreler)
            sonuclar = self.curs.fetchall()
            self.tblw_Liste.clearContents() #içerikleri temizle
            self.tblw_Liste.setRowCount(0) #satır sayısını sıfırla
            
            # Sonuçları tabloya ekler
            for satirIndeks, satirVeri in enumerate(sonuclar):
                self.tblw_Liste.insertRow(satirIndeks)
                for sutunIndeks, sutunVeri in enumerate(satirVeri):
                    self.tblw_Liste.setItem(satirIndeks,sutunIndeks,
                                            QTableWidgetItem(str(sutunVeri)))
        else:
            QMessageBox.warning(None, "Uyarı","Aramak için TC veya cep no giriniz.")
            
    # Seçili kaydı silmek için kullanılan metod        
    def kayit_sil(self):
        
        # Kullanıcıya kaydı silmek isteyip istemediğini sorar
        cevap = QtWidgets.QMessageBox().question(self,"KAYIT SİL","Kaydı silmek istiyor musunuz ?",QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if cevap == QtWidgets.QMessageBox.Yes:
            secili = self.tblw_Liste.selectedItems() # Seçili öğeleri alır
            if secili:
                silinicek = secili[5].text() # Silinecek kaydın TC numarasını alır
                try:
                    
                    # Kaydı siler
                    self.curs.execute("DELETE FROM buro WHERE  MuvekkilTCNo=?",
                 (silinicek,))
                    self.conn.commit()
                    self.listele() # Tabloyu günceller 
                    self.statusbar.showMessage("Kayıt başarıyla silindi.",10000)
                except sqlite3.Error as hata:
                    self.statusbar.showMessage("Hata oluştu:" + str(hata))
            else:
                self.statusbar.showMessage("Silinecek Kaydı Seçin ",10000)
        else:
             self.statusbar.showMessage("Silme İşlemi İptal Edildi.",10000)
     
             
    # Hakkında bilgilerini göstermek için kullanılan metod 
    def hakkinda_goster(self):
        
        # Hakkında bilgilerini göstermek için bir diyalog penceresi oluşturur
        self.hakkinda_dialog = QDialog() 
        # Oluşturduğu diyalog penceresine Ui_hakkinda sınıfından bir örnek ekler
        self.ui_hakkinda = Ui_hakkinda()
        self.ui_hakkinda.setupUi(self.hakkinda_dialog)
        # Diyalog penceresini gösterir
        self.hakkinda_dialog.exec_()

            
    def cikis(self):
        # Programı kapatır
        self.close()
        
    def closeEvent(self, event):
        #Kullanıcıya programdan çıkmak isteyip istemediğini sorar
        cevap = QMessageBox.question(self,"ÇIKIŞ","Programdan çıkmak istiyor musunuz?",
                                        QMessageBox.Yes  | QMessageBox.No)
        if cevap == QMessageBox.Yes:
            self.conn.close() # Veritabanı bağlantısını kapatır
            event.accept()
        else:
            event.ignore() # Kullanıcının çıkış işlemini iptal eder
            
           
           
if __name__ =="__main__":
    import sys 
    app = QtWidgets.QApplication(sys.argv)  # PyQt uygulamasını başlatır
    sifre_giris = Ui_sifreleme_class()  # Ana pencere sınıfından bir örnek oluşturur
    sifre_giris.show() # Oluşturulan ana pencereyi gösterir
    sys.exit(app.exec_())  # PyQt uygulamasını başlatır ve kontrolü event loop'a bırakır