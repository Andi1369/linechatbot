import sqlite3
import numpy as np
import pandas as pd
import ast

class DB:
    def __init__(self):
        self.initDB()

    def initDB(self):
        self.conn = sqlite3.connect("database.db")

    def select(self):
        return self.conn.execute("SELECT * from `hasil_preprocessing`")

    def closeDB(self):
        self.conn.close()    


class Process():
    def __init__(self,data):    
        self.data = data
        self.limit_per_jawaban = 20
        self.result = self.proc()

    def levenshtein(self, seq1, seq2):
        if(seq1 == seq2):
            return 0
        size_x = len(seq1) + 1
        size_y = len(seq2) + 1
        matrix = np.zeros ((size_x, size_y))
        for x in range(size_x):
            matrix [x, 0] = x
        for y in range(size_y):
            matrix [0, y] = y

        for x in range(1, size_x):
            for y in range(1, size_y):
                if seq1[x-1] == seq2[y-1]:
                    matrix [x,y] = min(
                        matrix[x-1, y] + 1,
                        matrix[x-1, y-1],
                        matrix[x, y-1] + 1
                    )
                else:
                    matrix [x,y] = min(
                        matrix[x-1,y] + 1,
                        matrix[x-1,y-1] + 1,
                        matrix[x,y-1] + 1
                    )
        return (matrix[size_x - 1, size_y - 1])

    def proc(self):
        p = DB()
        potentials = []
        for row in p.select():
            jawaban = row[1]
            keyworddb = row[2]
            keyworddb = ast.literal_eval(keyworddb)
            counterjawaban = 0
            for target in self.data:   
                targetarr = [] 
                for key in keyworddb:
                    res = self.levenshtein(key, target)
                    targetarr.append(res)
                    if(res == 0):    
                        break
                counterjawaban += min(targetarr)
                if(counterjawaban >= self.limit_per_jawaban):    
                    break 

            potential = {
                'val' : counterjawaban,
                'jawaban' : jawaban
            }
            potentials.append(potential)
        p.closeDB()
        
        min_val = potentials[0]['val']
        min_index = 0
        for i in range(0,len(potentials)):
            potential = potentials[i]
            if (potential['val'] < min_val):
                min_val = potential['val']
                min_index = i        
        return potentials[min_index]
  