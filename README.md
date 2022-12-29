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


