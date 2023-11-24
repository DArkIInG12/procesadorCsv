import pandas as pd
import os

class CsvFile:

    df = None

    def __init__(self,file):
        self.route = "{}".format(file)
        if os.path.exists(self.route):
            self.df = pd.read_csv(self.route)
            self.df = self.df.dropna()
        else:
            print("El archivo no existe en la ruta indicada")
            df = pd.DataFrame()
            df.to_csv(self.route)
            self.df = pd.read_csv(self.route)
            print("Arhivo",file,"creado")

    def select(self):
        if self.df is not None:
            indexes = self.df.index.to_list()
            headers = self.df.columns.to_list()
            data = self.df.values.tolist()
            data.insert(0,[headers,indexes])
            return data
        else:
            print("No se puede leer el archivo")
    
    def insert(self,headers,data,a_index):
        new_row = {}
        if self.df is not None:
            for i in range(len(headers)):
                new_row[headers[i]] = data[i]
            aux_df = pd.DataFrame([new_row],index=[a_index])
            self.df = pd.concat([self.df, aux_df])
            self.df.to_csv(self.route,index=False)
        else:
            print("No se puede leer el archivo")
        
    def update(self,index,headers,data):
        if self.df is not None:
            for i in range(len(headers)):
                self.df.loc[index,headers[i]] = data[i]
            self.df.to_csv(self.route,index=False)
        else:
            print("No se puede leer el archivo")

    def delete(self,index):
        if self.df is not None:
            self.df = self.df.drop(index)
            self.df.to_csv(self.route,index=False)
        else:
            print("No se puede leer el archivo")
