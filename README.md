# Air Pressure Sensor Fault Detection.
Designed and implemented an end-to-end scalable and deployable pipeline which can ingest, validate, transform data followed by model training and evaluation stages for identifying faulty sensor components in the air pressure systems in automobiles.

## Key Capabilities.
-> Automated data drift detection.  
-> Automated the process of dealing imbalanced data.  
-> Automated statistical analysis reports creation in various stages of pipeline artifacts.  

# File Structure
```
Air pressure sensor fault detection
    |
    |
    |-- DATA VISUALIZATION -- |
    |                         |-- Data_viz.ipynb              # Data Visualization and workflow outline.
    |
    |-- SENSOR -- |
    |             |-- init.py
    |             |-- config.py                               # Includes access key to env variables.
    |             |-- exception.py                            # Traceback and exception reporting
    |             |-- logger.py                               # Logging module.
    |             |-- predictor.py                            # Model and binary file locator. 
    |             |-- utils.py                                # Contains widely used helper functions.
    |             |
    |             |-- COMPONENTS --|
    |             |                |
    |             |                |-- init.py
    |             |                |-- Data_Ingestion.py      # DATA COLLECTION. 
    |             |                |-- Data_Transformation.py # DATA PRE-PROCESSING. 
    |             |                |-- Data_validation.py     # VALIDATE DATA FOR BEFORE PREPROCESSING.
    |             |                |-- Model_evaluation.py    # EVALUATE MODELS.
    |             |                |-- Model_pusher.py        # DEPLOYMENT.
    |             |                |-- Model_trainer.py       # TRAIN DATA ON A MODEL.
    |             |
    |             |-- ENTITY --|
    |             |            |-- init.py
    |             |            |-- artifact_entity.py         # Output of a DSLC component (dataclass).
    |             |            |-- config_entity.py           # Input of a DSLC component.
    |             |
    |             |-- PIPELINE --|
    |                            |-- init.py
    |                            |-- training_pipeline.py
    |                            |-- batch_prediction.py
    |
    |-- .gitignore
    |-- Dataset                                               # .csv file.
    |-- data_dump.py                                          # Dumps data (.csv) to database.
    |-- logger_and_exception_tester.py                        # Testig logger and exception module.
    |-- main.py                                               # initiation of the project.
    |-- README.md                                             # About the project.
    |-- requirements.txt                                      # Required libraries for the project.
    |-- setup.py                                              # Package creator / requirement getter.
```


