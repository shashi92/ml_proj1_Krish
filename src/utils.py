import os, sys
import numpy as np
import pandas as pd
from src.logger import logging
from src.exception import CustomException
import dill 
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV
import pickle

from sklearn.metrics import r2_score


def save_object(file_path, obj):
    try:
        dirName = os.path.dirname(file_path)
        os.makedirs(dirName, exist_ok=True)
        
        with open(file_path, 'wb') as f:
            dill.dump(obj, f)
            
    except Exception as e:
        raise CustomException(e, sys)

def load_object(file_path):
    try:
        
        with open(file_path, 'rb') as f:
            return pickle.load(f)
        
    except Exception as e:
        raise CustomException(e, sys)  
        
def evaluate_model(Xtrain, ytrain, Xtest, ytest, models:dict, param: dict):
    try:
        report = {}
        
        for i in range(len(list(models))):
            model=list(models.values())[i]
            para = param[list(models.keys())[i]]
            # para = param[list(models.keys())[i]]
            rs = GridSearchCV(model, para, cv=3)
            rs.fit(Xtrain, ytrain)
            model.set_params(**rs.best_params_)
            model.fit(Xtrain, ytrain)
            ytest_pred = model.predict(Xtest)
            r2_test = r2_score(ytest, ytest_pred)
            
            report[list(models.keys())[i]] =  r2_test
            
        return report
             
    except Exception as e:
        raise CustomException(e, sys)
    