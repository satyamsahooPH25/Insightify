import sys
import tensorflow as tf
import os
sys.path.append(r"C:\Users\satya\Desktop\Insightify\Code_base\Version_0.1")
from Tokenizer_Embedder import Vectorizer
class Predictor:
    def __init__(self):
        self.vectorizer=Vectorizer()
        self.path={}
        root_directory = r'C:\Users\satya\Desktop\Insightify\Code_base\Version_0.1'
        self.model_paths = []
        for root, dirs, files in os.walk(root_directory):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                if os.path.isdir(dir_path):
                    self.model_paths.append(dir_path)
        self.txt_file_paths = []
        for item in os.listdir(root_directory):
            full_path = os.path.join(root_directory, item)
            if os.path.isfile(full_path) and full_path.endswith('.txt'):
                self.txt_file_paths.append(full_path)
        for model,categories in zip(self.model_paths,self.txt_file_paths):
            self.path[tf.saved_model.load(model)]=categories

    def predict(self,text):
        self.model_output={'Classification':[],'Data Cleaning':[],'EDA':[],'Model Evaluation':[],'Regression':[],'Different':[]}
        vector=self.vectorizer.transform_text(text)
        model_dict=self.path
        for model_ in model_dict:
            inference_fn = model_.signatures['serving_default']
            predictions = inference_fn(vector)
            predictions = predictions[list(predictions.keys())[0]].numpy()[0]
            with open(model_dict[model_], 'r') as file:
                count=0
                for line in file:
                    category = line.strip()
                    self.model_output[category].append(predictions[count])
                    count+=1
        max_pred=0
        max_cat=''
        for i in self.model_output:
            self.model_output[i]=sum(self.model_output[i])/len(self.model_output[i])
            if max_pred<self.model_output[i]:
                max_pred=self.model_output[i]
                max_cat=i


        return max_cat,self.model_output,max_pred 