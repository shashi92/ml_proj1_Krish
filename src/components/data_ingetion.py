from dataclasses import dataclass
import os
import sys
# sys.path.append('C:/Users/shashiAdmin/A python learnbay/VS/ml_proj1_Krish') 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.exception import CustomException
from src.logger import logging
from src.components.data_transformation import DataTransformation, DataTransformConfig
from src.components.model_train import ModelTrainer

import pandas as pd
from sklearn.model_selection import train_test_split

@dataclass
class DataIngestionConfig:
    train_data_path = os.path.join('artifacts', 'train.csv')
    test_data_path = os.path.join('artifacts', 'test.csv')
    raw_data_path = os.path.join('artifacts', 'data.csv')

class DataIngestion:
    def __init__(self) -> None:
        self.ingestion_config = DataIngestionConfig()
    
    def initate_ingestion(self):
        try:
            logging.info("In data ingestion")  
            df = pd.read_csv('notebook\data\stud.csv')
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logging.info('raw file created')
            train_set, test_set = train_test_split(df, test_size=0.3, random_state=42)
            train_set.to_csv(self.ingestion_config.train_data_path, header=True, index=False)
            test_set.to_csv(self.ingestion_config.test_data_path, header=True, index=False)
            logging.info("train test split and stored successfully")
            return (self.ingestion_config.train_data_path, self.ingestion_config.test_data_path )
        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    obj = DataIngestion()
    train_path, test_path = obj.initate_ingestion()
    data_transform = DataTransformation()
    train_data,test_data, _ = data_transform.initializeTransformation(train_path, test_path)
    model_train = ModelTrainer()
    r2_score, best_model_name = model_train.initate_model_trainer(train_array= train_data, test_array = test_data)
    print(r2_score, best_model_name)
    
        
    