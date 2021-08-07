from preprocess import Preprocess
from process import Process

coba = "apa isi dekret presiden ?"
coba = Preprocess (coba)

coba = coba.result
coba = Process (coba)