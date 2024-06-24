import pandas as pd

class Txt2Excel:
    Qdict = {}
    @classmethod
    def Dict_maker(self):
        key_num=int(input("Enter the number of keys"))
        for i in range(0,key_num):
            self.Qdict[input("enter key name")]=[]

    def __init__(self, input_txt, output_excel):
        self.input_txt = input_txt
        self.output_excel = output_excel
        self.Dict_maker()
        self.dict2Excel()

    def dict2Excel(self):
        self.Qdict=self.txt2dict()
        data = []
        for key, value_list in self.Qdict.items():
            for question in value_list:
                data.append({'Type': key, 'Question': question})
        df = pd.DataFrame(data)
        
        existing_df = pd.read_excel(self.output_excel)
        combined_df = pd.concat([existing_df, df], ignore_index=True)
        combined_df.to_excel(self.output_excel, index=False)

    def txt2dict(self):
        lines = self.txt2lines()
        reader = 0
        x = ""
        for line in lines:
            if ":" in line:
                x = line.split(":")[0].split('"')[1]
                reader = 1
            elif reader == 1:
                if "]" in line:
                    reader = 0
                if reader == 1:
                    self.Qdict[x].append(line.split('"')[1])
        return self.Qdict
    
    def txt2lines(self):
        with open(self.input_txt, 'r') as file:
            return file.readlines()
