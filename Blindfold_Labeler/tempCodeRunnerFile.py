import pandas as pd
import numpy as np
class Blindfold:
    def __init__(self,df,cat_col):
        self.df=df
        self.cat_col=cat_col
        self.Label_Distributor={}
    def splitter(self,cat):
        def Differ(x):
            return "Different"
        change = self.df[self.df[self.df.columns[self.cat_col]]!=cat].sample(frac=1) 
        change.iloc[:,self.cat_col] = change.iloc[:,self.cat_col].apply(Differ)
        return self.df[self.df[self.df.columns[self.cat_col]]==cat],change 
    def categoriser(self,cat):
        cat_val,Different_val=self.splitter(cat)
        cat_val_len=cat_val.shape[0]
        Different_val_len=Different_val.shape[0]
        Different_stack=[]
        start=0
        end = cat_val_len
        for i in range(Different_val_len//cat_val_len):
            Different_stack.append(Different_val.iloc[start:end])
            start=end
            end=start+cat_val_len
        Different_stack.append(Different_val.iloc[start:Different_val_len]) 
        for i in range(cat_val_len-(Different_val_len%cat_val_len)):
           Different_stack[-1]=pd.concat([Different_stack[-1],pd.DataFrame(Different_val.iloc[np.random.randint(0,Different_val.shape[0],1)])],ignore_index=True)   
        Output=[]
        for i in Different_stack:
            i=pd.concat([i,cat_val],ignore_index=True)
            Output.append(i)
        return Output
    def Dict_Cat(self):
        Dict = {}
        count = 0 
        for i in self.df[self.df.columns[self.cat_col]].unique():
            cat_data = self.categoriser(i)
            for k in cat_data:
                Dict[i + str(count)] = k
                count += 1  
            count=0
        return Dict




    

    

        
         