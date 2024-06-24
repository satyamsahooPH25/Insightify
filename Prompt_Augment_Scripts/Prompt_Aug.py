import pandas as pd
from nltk.corpus import wordnet
import random
from nlpaug.augmenter.word import (SpellingAug, ContextualWordEmbsAug)
class Augmenter:
    def __init__(self,df,output_excel):
        self.df=df
        self.output_excel = output_excel
        self.output_df = pd.read_excel(self.output_excel)
        self.output_df_prompts=list(self.output_df["Question"])
        self.output_df_categories=list(self.output_df["Type"])
        self.output_df_ID = list(self.output_df["ID"])
        self.prompts=list(df[df.columns[1]])
        self.categories=list(df[df.columns[0]])
        self.prompt_category_dictionary={prompt:category for prompt,category in zip(self.prompts,self.categories)}
        self.Contextual_Aug()
        self.synonym()
        self.Scrambller()
        
    def synonym(self):
        def get_synonyms_cached(word,synonyms_cache={}):
            if word not in synonyms_cache:
                synonyms_cache[word]=wordnet.synsets(word)
            return synonyms_cache[word]
        def generate_augmented_prompts(prompt):
            augmented_prompts = []
            for i, word in enumerate(prompt.split()):
                synonyms = get_synonyms_cached(word)
                if synonyms:  
                    augmented_prompts.extend([prompt.replace(word, synonym.lemmas()[0].name()) for synonym in synonyms])
                else:
                    augmented_prompts.append(prompt)
                return augmented_prompts
        for prompt in self.prompt_category_dictionary:
            if prompt in self.output_df_prompts and self.output_df_ID[self.output_df_prompts.index(prompt)]=="synonym":
              print("synonym_augmentation of row",self.prompts.index(prompt),"PRE-completed")
              continue
            self.output_df_prompts.append(prompt) 
            self.output_df_categories.append(self.prompt_category_dictionary[prompt])
            self.output_df_ID.append("synonym")
            augmented_prompts = generate_augmented_prompts(prompt)
            for aug_prompt in augmented_prompts:
                if(aug_prompt not in self.prompts):
                    self.output_df_prompts.append(aug_prompt) 
                    self.output_df_categories.append(self.prompt_category_dictionary[prompt])
                    self.output_df_ID.append("synonym")
                    print("synonym_augmentation of row",self.prompts.index(prompt),"processing")
            self.dict2Excel()
            print("synonym_augmentation of row",self.prompts.index(prompt),"completed")
    
    def Contextual_Aug(self):
         for prompt in self.prompt_category_dictionary :
            if prompt in self.output_df_prompts and self.output_df_ID[self.output_df_prompts.index(prompt)]=="Contextual_Aug":
              print("Contextual_augmentation of row",self.prompts.index(prompt),"PRE-completed")
              continue
            augmented_prompts=[prompt]
            contextual_aug = ContextualWordEmbsAug(model_path='bert-base-uncased')
            self.output_df_prompts.append(prompt) 
            self.output_df_categories.append(self.prompt_category_dictionary[prompt])
            self.output_df_ID.append("Contextual_Aug")
            for i in range(5):
                if contextual_aug.augment(augmented_prompts[0]) not in augmented_prompts:
                    augmented_prompts.append(contextual_aug.augment(augmented_prompts[0]))
            for aug_prompt in augmented_prompts:
                if(aug_prompt[0] not in self.prompts):
                    print(aug_prompt)
                    self.output_df_prompts.append(aug_prompt[0]) 
                    self.output_df_categories.append(self.prompt_category_dictionary[prompt])
                    self.output_df_ID.append("Contextual_Aug")
                    print("Contextual_augmentation of row",self.prompts.index(prompt),"processing")
            self.dict2Excel()
            print("Contextual_augmentation of row",self.prompts.index(prompt),"completed")
    
    def Scrambller(self):
        aug = SpellingAug(dict_path=None, aug_p=0.2)
        for prompt in self.prompt_category_dictionary:
          if prompt in self.output_df_prompts and self.output_df_ID[self.output_df_prompts.index(prompt)]=="Scrambler":
              print("Scramble_augmentation of row",self.prompts.index(prompt),"PRE-completed")
              continue
          self.output_df_prompts.append(prompt) 
          self.output_df_categories.append(self.prompt_category_dictionary[prompt])
          self.output_df_ID.append("Scrambler")
          aug_prompt = aug.augment(prompt)
          if(aug_prompt not in self.prompts):
                    self.output_df_prompts.append(aug_prompt) 
                    self.output_df_categories.append(self.prompt_category_dictionary[prompt])
                    self.output_df_ID.append("Scrambler")
                    print("Scramble_augmentation of row",self.prompts.index(prompt),"processing")
          self.dict2Excel()
          print("Scramble_augmentation of row",self.prompts.index(prompt),"completed")
        
    def dict2Excel(self):
        existing_df = pd.read_excel(self.output_excel)
        combined_df = pd.concat([existing_df, pd.DataFrame(list(zip(self.output_df_categories,self.output_df_prompts,self.output_df_ID)),columns=["Type","Question","ID"])], ignore_index=True)
        if combined_df.duplicated().sum()>0:
            print("Duplicate",combined_df.duplicated().sum())
            combined_df.drop_duplicates(inplace=True,keep='first')
        combined_df.to_excel(self.output_excel, index=False)



          

        
        
