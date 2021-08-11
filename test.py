from preprocess import Preprocess
from process import Process

coba = "Apa latar belakang munculnya penjajahan samudra oleh bangsa Eropa ?"
coba = Preprocess (coba)

coba = coba.result
coba = Process (coba)