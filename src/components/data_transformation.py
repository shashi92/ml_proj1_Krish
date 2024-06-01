from dataclasses import dataclass
import os, sys
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import numpy as np
import pandas as pd
from src.logger import logging
from src.exception import CustomException
from src.utils import save_object

@dataclass
class DataTransformConfig:
    preprocessor_obj_file_path = os.path.join("artifacts", "preprocessor.pkl")
    
class DataTransformation:

        def __init__(self) -> None:
            self.data_transformation_config = DataTransformConfig()
            
        
        def get_data_transformer_obj(self):
            try:
                numerical_cols = ['reading_score', 'writing_score']
                cat_cols = ['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch',
                            'test_preparation_course']
                
                num_pipline = Pipeline([
                    ("imputer", SimpleImputer(strategy='median')),
                    ("scaler", StandardScaler(with_mean=False))
                ])
                cat_pipline = Pipeline([
                    ("imputer", SimpleImputer(strategy='most_frequent')),
                    ("OHencoer", OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean=False))
                ])
                
                preprocessor = ColumnTransformer([
                    ('numpipeline', num_pipline, numerical_cols),
                    ('catpipline', cat_pipline, cat_cols)
                ])   
                return preprocessor
                
            except Exception as e:
                raise CustomException(e, sys)
        
        def initializeTransformation(self, train_path, test_path):
            try:
                train_df = pd.read_csv(train_path)
                test_df = pd.read_csv(test_path)
                
                
                preprocessing_obj = self.get_data_transformer_obj()
                target = "math_score"
                
                X_train = train_df.drop(columns=[target], axis=1)
                y_train = train_df[target]
                
                X_test = test_df.drop(columns=[target], axis=1)
                y_test = test_df[target]
                
                X_train_pre = preprocessing_obj.fit_transform(X_train)
                X_test_pre = preprocessing_obj.fit_transform(X_test)
                
                train_arr = np.c_[X_train_pre, np.array(y_train)]
                test_arr = np.c_[X_test_pre, np.array(y_test)]
                
                logging.info("Saved preprocessing object")
                save_object(
                    file_path = self.data_transformation_config.preprocessor_obj_file_path,
                    obj = preprocessing_obj
                )
                return(
                    train_arr, 
                    test_arr, 
                    self.data_transformation_config.preprocessor_obj_file_path
                )
                
            except Exception as e:
                raise CustomException(e, sys)

            
            
            

        
    
    
    
    