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
    |                         |-- Data_viz.ipynb
    |
    |-- SENSOR -- |
    |             |-- init.py
    |             |-- config.py
    |             |-- exception.py
    |             |-- logger.py
    |             |-- predictor.py
    |             |-- utils.py
    |             |
    |             |-- COMPONENTS --|
    |             |                |
    |             |                |-- init.py
    |             |                |-- Data_Ingestion.py
    |             |                |-- Data_Transformation.py
    |             |                |-- Data_validation.py
    |             |                |-- Model_evaluation.py
    |             |                |-- Model_pusher.py
    |             |                |-- Model_trainer.py
    |             |
    |             |-- ENTITY --|
    |             |            |-- init.py
    |             |            |-- artifact_entity.py
    |             |            |-- config_entity.py
    |             |
    |             |-- PIPELINE --|
    |                            |-- init.py
    |                            |-- training_pipeline.py
    |                            |-- batch_prediction.py
    |
    |-- .gitignore
    |-- Dataset
    |-- data_dump.py
    |-- logger_and_exception_tester.py
    |-- main.py
    |-- README.md
    |-- requirements.txt
    |-- setup.py
```


