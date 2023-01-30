from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    feature_store_dir:str
    train_file_path:str
    test_file_path:str

@dataclass
class DataValidationArtifact:
    report_file_path:str

@dataclass
class DataTransformationArtifact:
    transform_object_path:str
    transformed_train_path:str
    transformed_test_path:str
    target_encoder_path:str

@dataclass
class ModelTrainerArtifact:
    model_path:str
    f1_train_score:str
    f1_test_score:str

@dataclass
class ModelEvaluationArtifact:
    model_accepted:bool
    improved_accuracy_score:float
@dataclass
class ModelPusherArtifact:
    pusher_model_dir:str
    saved_model_dir:str