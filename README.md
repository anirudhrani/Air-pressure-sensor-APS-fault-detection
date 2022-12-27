# File Structure
**Air pressure sensor fault detection** <br>
| <br>
|-- **DATA VISUALIZATION** -- |  <br>
|                             |-- Data_viz.ipynb   <br>
| <br>
|-- **SENSOR** -- | <br>
|                 |-- init.py <br>
|                 |-- config.py <br>
|                 |-- exception.py <br>
|                 |-- logger.py <br>
|                 |-- predictor.py <br>
|                 |-- utils.py <br>
|                 | <br>
|                 |-- **COMPONENTS** --| <br>
|                 |                    | <br>
|                 |                    |-- init.py <br>
|                 |                    |-- Data_Ingestion.py <br>
|                 |                    |-- Data_Transformation.py <br>
|                 |                    |-- Data_validation.py <br>
|                 |                    |-- Model_evaluation.py <br>
|                 |                    |-- Model_pusher.py <br>
|                 |                    |-- Model_trainer.py <br>
|                 | <br>
|                 |-- **ENTITY** --| <br>
|                 |                |-- init.py <br>
|                 |                |-- artifact_entity.py <br>
|                 |                |-- config_entity.py <br>
|                 | <br>
|                 |-- **PIPELINE** --| <br>
|                                    |-- init.py            <br>                 
|                                    |-- training_pipeline.py <br>
|                                    |-- batch_prediction.py <br>
|
|-- Dataset <br>
|-- data_dump.py <br>
|-- logger_and_exception_tester.py <br>
|-- main.py <br>
|-- README.md <br>
|-- requirements.txt <br>
|-- setup.py         <br>
          


