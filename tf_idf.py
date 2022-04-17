from re import findall, sub
from math import log
from stopword import stopword

# class tfidf
class TfIdf:
    def __init__(self, kalimat):
        # untuk menyimpan kalimat awal
        self.kalimat = kalimat
        # array menyimpan hasil casefold
        self.casefold = []
        # array menyimpan hasil pemisahan berdasarkan .
        self.perkalimat = []
        # array menyimpan hasil filter
        self.filter = []
        # array menyimpan hasil token (memecah menjadi array per-kata)
        self.token = []
        # array menyimpan hasil stopword (menghilangkan stopword)
        self.stopword_val = []
        # array menyimpan kata-kata yang unik saja
        self.unique = []
        # arary menyimpan jumlah kemunculan kata-kata unik dalam dokumen ini saja
        self.frekuensi_term = {}
        # arary menyimpan jumlah kemunculan kata-kata unik dalam dokumen ini saja, namun dengan lengkap di kalimat mana
        self.frekuensi_term_perkalimat = {}
        # arary menyimpan jumlah kemunculan kata-kata unik dalam semua dokumen  **tidak terpakai sejauh ini
        self.dokumen_term = {}
        # arary menyimpan jumlah kemunculan kata-kata unik dalam semua dokumen tapi dispesifikan perdokumen**tidak terpakai sejauh ini
        self.dokumen_term_perdoc = {}
        # nilai idf, dan tfidf
        self.idf_val = {}
        self.tf_val = {}
        self.tf_idf_val = {}

    # function process, function yang dipanggil di document.py
    def process(self):
        self.case_folding()
        self.pemecah_kalimat()
        self.filtering()
        self.stopword_removal()
        self.tokenizing()
        self.set_unique()
        self.set_frekuensi_term()

    # huruf kecil
    def case_folding(self):
        self.case_fold = self.kalimat.casefold()

    # misahin berdasarkan titik
    def pemecah_kalimat(self):
        # function sub untuk mengganti parameter1, keparameter2 pada parameter3
        # dalam kasus ini mengganti enter menjadi spasi pada var self.case_fold, 
        # keluaraanya masuk one_liner
        one_liner = sub('(\r\n)|[\r\n]', ' ', self.case_fold)
        # misahan berdsarkan .
        kalimat_pecahan = one_liner.split('.')
        for index, line in enumerate(kalimat_pecahan):
            self.perkalimat.append(line)

    # filter symbol, ngilangin spasi lebih
    def filtering(self):
        for index, line in enumerate(self.perkalimat):
            filter_kalimat = sub('[\d+\!\(\<\]\@\)\:\|\#\.\;\\\$\,\/\+\%\„\?\=\^\"\{\_\&\}\,\*\>\[\t\r\n(\(.*\))]|(\d+\/\d+\/\d+)', '', line)
            # mengubah - atau spasi yang leibh dari 1 menjadi 1 spasi
            filter_kalimat = sub('[\-|\s{2,}]', ' ', filter_kalimat)
            # menghilangkan spasi di awal dan di akhir
            filter_kalimat = sub('(^\s+|\s+$)(.*)', r'\2', filter_kalimat)
            if filter_kalimat:
                self.filter.append(filter_kalimat)     

    # menghilangkan kata-kata yang tidak penting
    def stopword_removal(self):
        stopwords = stopword.get_stopwod_stringed()
        for index, line in enumerate(self.filter):
            remove_stopword = sub(stopwords, '', line)
            self.stopword_val.append(remove_stopword)

    # memecah kata-kata menjadi array
    def tokenizing(self):
        for index, line in enumerate(self.stopword_val):
            tokenize = line.split()
            self.token.append(tokenize)

    # mengambil kata-kata yang unik saja
    def set_unique(self):
        self.unique = self.token.copy()
        unique = self.unique[0].copy()
        for i in range(1, len(self.unique)):
            for index, word in enumerate(self.unique[i]):
                if word not in unique:
                    unique.append(word)
        self.unique = unique

    # menghitung jumlah kemunculan kata-kata pada kalimat-kalimat
    def set_frekuensi_term(self):
        # unique = ['rencana', 'jakarta']
        for i, iv in enumerate(self.unique):
            nums = [] # S0: 1, S2: 2, S3: 0, ..., S7: 0
            total = 0
            for l, lv in enumerate(self.stopword_val):
                num = 0
                regex = '\\b%s\\b' % iv
                appear = findall(regex, lv) # return ['rencana', 'rencana']
                num = len(appear) # 2
                total += num
                nums.append(num)
            kamus = {}
            # kamus = {'asd': kv}
            for k, kv in enumerate(nums):
                kamus['S%d' % k] = kv
            self.frekuensi_term_perkalimat[iv] = kamus
            self.frekuensi_term[iv] = total

    def set_dokumen_term(self, dokumen_term):
        self.dokumen_term = dokumen_term.copy()
 
    def set_dokumen_term_perdoc(self, dokumen_term, doc_name):
        self.dokumen_term_perdoc[doc_name] = dokumen_term

    # Melakukan pengecekan array kata unique pada it_idf ini
    def check_doc_unique(self, unique):
        dokumen_term = {}
        for i, iv in enumerate(unique):
            nums = 0
            for l, lv in enumerate(self.stopword_val):
                regex = '\\b%s\\b' % iv
                appear = findall(regex, lv)
                num = len(appear)
                nums += num
            dokumen_term[iv] = nums;
        return dokumen_term

    def set_idf_value(self):
        # if len(self.dokumen_term_perdoc) == 0:
        n_doc = len(self.dokumen_term_perdoc) + 1
        for i in self.frekuensi_term:
            nDf = ( 1 if self.frekuensi_term[i] > 0 else 0 ) + self.dokumen_term[i]
            self.idf_val[i] = log(n_doc/nDf, 10)

    def set_tf_value(self):
        for i in self.frekuensi_term:
            if self.frekuensi_term[i] == 0:
                self.tf_val[i] = 0
            else:
                self.tf_val[i] = 1+log(self.frekuensi_term[i], 10)

    # menghitung tf-idf
    def set_tf_idf_value(self):
        for i in self.tf_val:
            self.tf_idf_val[i] = self.tf_val[i] * self.idf_val[i]
        
        
