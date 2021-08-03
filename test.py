from preprocess import Preprocess
from process import Process

coba = "siapa ketua bpupki ?"
coba = Preprocess (coba)

coba = coba.result
coba = Process (coba)