from preprocess import Preprocess
from process import Process

coba = "Kapan masa akhir order baru ?"
coba = Preprocess (coba)

coba = coba.result
coba = Process (coba)