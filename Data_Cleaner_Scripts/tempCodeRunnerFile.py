import pandas as pd
import copy
import nltk
import numpy as np
import pandas.api.types as pdt
class Column_Cleaner:
    def __init__(self,df,col_ind,start,end):
        self.df=df
        self.col_ind=col_ind
        self.start=start
        self.end=end
        self.char_code_classifier={}
    def is_sentence(self,string):
        words = nltk.word_tokenize(string)
        pos_tags = nltk.pos_tag(words)
        contains_noun = any(tag in ['NN', 'NNS', 'NNP', 'NNPS', 'PRP', 'PRP$'] for word, tag in pos_tags)
        contains_verb = any(tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'] for word, tag in pos_tags)
        if contains_noun and contains_verb:
            return True
        else:
            return False
    def dict_val_len(self,a):
        dict_len_list=[]
        for i in a:
            dict_len_list.append(len(a[i]))
        return dict_len_list
    def char_code(self,char,alph,num):
        if(ord(char) in alph):
            return 'A'
        elif(ord(char) in num):
            return 'N'
        else:
            return 'C'    
    def colImputer(self,a,new_keys):
        max_col_len = max(self.dict_val_len(a))
        for i in new_keys:
            for j in range(max_col_len-len(a[i])):
                a[i].insert(0,np.nan)
    def RowImputer(self,a):
        max_col_len = max(self.dict_val_len(a))
        for i in a:
            for j in range(max_col_len-len(a[i])):
                a[i].append(np.nan)
    def null_adder(self,a):
        for i in a:
            a[i].append(np.nan)
    def start_imputer(self,a,start_index):
        for i in a:
            for j in range(start_index):
                a[i].insert(0,np.nan)
    def df_create(self,val_list,column_keys,col_ind,df,sep,symbols_keys):
        new_keys=[]
        count_num=0
        print(val_list)
        for num,i in enumerate(val_list):
            col_name=list(i.keys())[0]
            if i[col_name] =='A':
                if col_name in list(column_keys.keys()):
                                column_keys[col_name].append(col_name)
                else:
                                column_keys[col_name]=[]
                                column_keys[col_name].append(col_name)
                                new_keys.append(col_name)
                                sep.append(i[col_name])
            elif i[col_name] =='N':
                if df.columns[col_ind]+str(count_num) not in column_keys:
                    column_keys[df.columns[col_ind]+str(count_num)]=[str(col_name)]
                    new_keys.append(df.columns[col_ind]+str(count_num))
                    count_num+=1
                    sep.append(i[col_name])
                else:
                    column_keys[df.columns[col_ind]+str(count_num)].append(str(col_name))
                    count_num+=1
            elif i[col_name] == 'C' and (col_name in symbols_keys) :
                column_keys[col_name]=[]
                column_keys[col_name].append(col_name)
                sep.append(i[col_name])
                new_keys.append(col_name)
        self.colImputer(column_keys,new_keys)
        self.RowImputer(column_keys)
    def collimator(self,column_keys,sep):
        coll1=['N','C','N']
        coll2=['A','C','A']
        to_delete=[]
        print(list(column_keys.keys()))
        while len(sep)>len(list(column_keys.keys())):
            sep.pop()
        for num in range(1,len(sep)-1):
            a=sep[num-1]
            b=sep[num]
            c=sep[num+1]
            bool1 = (a == coll1[0])and(b == coll1[1])and(c == coll1[2])
            bool2 = (a == coll2[0])and(b == coll2[1])and(c == coll2[2])
            column_keys_list = list(column_keys.keys())
            column_keys_len = len(column_keys[column_keys_list[num]])
            curr_col = column_keys[column_keys_list[num]]
            prev_col = column_keys[column_keys_list[num-1]]
            post_col = column_keys[column_keys_list[num+1]]
            if bool1 and ('.' in curr_col or ',' in curr_col) :
                    sym_impute=''
                    if('.' in curr_col):sym_impute='.'
                    else:sym_impute=','
                    for j in range(column_keys_len):
                        pre=prev_col[j]
                        pres=curr_col[j]
                        post=post_col[j]
                        if(str(pre)!='nan' and str(post)!='nan' and str(pres)=='nan'):
                            pres=sym_impute
                        modify=[pre,pres,post]
                        update=''
                        for i in modify:
                            if sym_impute=='.':
                                if str(i)!='nan':
                                    update+=str(i)
                            else:
                                if str(i)!='nan' and str(i)!=',':
                                    update+=str(i)
                        if len(update)!=0:
                            curr_col[j]=update
                            prev_col[j]=update
                            post_col[j]=update
                        else:
                            curr_col[j]=np.nan
                        to_delete.extend([num-1,num+1])
            elif bool2 and ' ' in curr_col:
                    for j in range(column_keys_len):
                        pre=prev_col[j]
                        pres=curr_col[j]
                        post=post_col[j]
                        if(str(pre)!='nan' and str(post)!='nan' and str(pres)=='nan'):
                            pres=' '
                        modify=[pre,pres,post]
                        print(modify)
                        update=''
                        for i in modify:
                            if str(i)!='nan':
                                update+=i
                        if len(update)!=0:
                            curr_col[j]=update
                            prev_col[j]=update
                            post_col[j]=update
                        else:
                            curr_col[j]=np.nan
                        to_delete.extend([num-1,num+1])
        column_keys_list = list(column_keys.keys())
        for num in to_delete:
            try:
                del column_keys[column_keys_list[num]]
            except:
                pass
    def Clean_Column(self):
        if pdt.is_integer_dtype(self.df.iloc[self.start:self.end,self.col_ind]) or pdt.is_float_dtype(self.df.iloc[self.start:self.end,self.col_ind]):
             return self.df.iloc[self.start:self.end,self.col_ind],None 
        alphabet=list(range(97,123))+list(range(65,91))
        number=range(48,58)
        currency_symbols = {
            "€": ("Euro", 8364, "EUR"),
            "£": ("Pound Sterling", 163, "GBP"),
            " Kč": ("Czech Koruna", 7520, "CZK"),
            "CHF": ("Swiss Franc", 6776, "CHF"),
            "SEK": ("Swedish Krona", 8360, "SEK"),
            "DKK": ("Danish Krone", 8361, "DKK"),
            "NOK": ("Norwegian Krone", 8362, "NOK"),
            "PLN": ("Polish Złoty", 8301, "PLN"),
            "HUF": ("Hungarian Forint", 7046, "HUF"),
            "$": ("US Dollar", 36, "USD"),
            "$": ("Canadian Dollar", 36, "CAD"),
            "$": ("Mexican Peso", 36, "MXN"),
            "R$": ("Brazilian Real", 8364, "BRL"),
            "ARS": ("Argentine Peso", 8365, "ARS"),
            "COP": ("Colombian Peso", 8351, "COP"),
            "CLP": ("Chilean Peso", 8352, "CLP"),
            "PEN": ("Peruvian Sol", 8363, "PEN"),
            "¥": ("Japanese Yen", 165, "JPY"),
            "₩": ("South Korean Won", 8369, "KRW"),
            "₹": ("Indian Rupee", 8377, "INR"),
            "฿": ("Thai Baht", 3647, "THB"),
            "IDR": ("Indonesian Rupiah", 8360, "IDR"),
            "PHP": ("Philippine Peso", 8365, "PHP"),
            "VND": ("Vietnamese Dong", 8363, "VND"),
            "ZAR": ("South African Rand", 8350, "ZAR"),
            "EGP": ("Egyptian Pound", 163, "EGP"),
            "NGN": ("Nigerian Naira", 8358, "NGN"),
            "KES": ("Kenyan Shilling", 7544, "KES"),
            "AUD": ("Australian Dollar", 65, "AUD"),
            "NZD": ("New Zealand Dollar", 36, "NZD"),
            "CHF": ("Swiss Franc", 6776, "CHF"),
            "ILS": ("Israeli New Shekel", 8362, "ILS"),
            " zł": ("Polish Złoty", 322, "PLN"),
            "₩": ("South Korean Won", 8369, "KRW"),
            "元": ("Chinese Yuan Renminbi", 25881, "CNY"),
        }
        currency_symbols_keys = list(currency_symbols.keys())
        for i in currency_symbols:
            currency_symbols_keys.append(currency_symbols[i][2])
        currency_symbols_keys.extend([' ','.',','])
        symbols_keys=set(currency_symbols_keys)
        data=list(self.df.iloc[self.start:self.end,self.col_ind])
        for val_in_data in data:
             try:
                if(self.is_sentence(val_in_data)):
                    return self.df.iloc[self.start:self.end,self.col_ind],None
             except:
                  pass
        column_keys={}
        sep=[]
        index=-1
        start_index=-1
        flag=0
        for i in data:
            index+=1   
            code=''
            prev_char_code=''
            emptyc=''
            emptya=''
            emptyn=''
            val_list=[]
            try:
                for num,k in enumerate(i):
                        if(prev_char_code!=self.char_code(k,alphabet,number)):
                            char_code_val=self.char_code(k,alphabet,number)
                            code+=char_code_val
                            prev_char_code=char_code_val
                            if(emptya!=''):
                                val_list.append({emptya:'A'})
                                emptya=''
                            if(emptyn!=''):
                                val_list.append({emptyn:'N'})
                                emptyn=''
                            if(emptyc!=''):
                                val_list.append({emptyc:'C'})
                                emptyc=''
                            if char_code_val == 'A':
                                emptya+=k
                            if char_code_val == 'C':
                                emptyc+=k
                            if char_code_val == 'N':
                                emptyn+=k
                            if num==len(i)-1:
                              if(emptya!=''):
                                val_list.append({emptya:'A'})
                                emptya=''
                              if(emptyn!=''):
                                val_list.append({emptyn:'N'})
                                emptyn=''
                              if(emptyc!=''):
                                val_list.append({emptyc:'C'})
                                emptyc=''
                        else:
                            char_code_val=self.char_code(k,alphabet,number)
                            if char_code_val == 'A':
                                emptya+=k
                            if char_code_val == 'C':
                                emptyc+=k
                            if char_code_val == 'N':
                                emptyn+=k
                            if num==len(i)-1:
                              if(emptya!=''):
                                val_list.append({emptya:'A'})
                                emptya=''
                              if(emptyn!=''):
                                val_list.append({emptyn:'N'})
                                emptyn=''
                              if(emptyc!=''):
                                val_list.append({emptyc:'C'})
                                emptyc=''
                            
            except:
                flag=1
                self.null_adder(column_keys)
            if(flag==0):
                self.df_create(val_list,column_keys,self.col_ind,self.df,sep,symbols_keys)
            flag=0
            if len(column_keys.keys()) and start_index==-1:
                start_index=index
            if(code in list(self.char_code_classifier.keys())):
                self.char_code_classifier[code].append(i)
            else:
                self.char_code_classifier[code]=[]
                self.char_code_classifier[code].append(i)
        self.start_imputer(column_keys,start_index)
        classified_col_values = copy.deepcopy(self.char_code_classifier)
        self.collimator(column_keys,sep)
        return pd.DataFrame(column_keys),classified_col_values
        
