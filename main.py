from src.core.usecases.extract_data_usecase import ExtractDataRawUsecase
from src.core.usecases.transform_data_usecase import TransformDataUsecase
from src.core.usecases.dump_data_usecase import DumpDataUsecase
from src.core.usecases.data_pipeline_usecase import DataPipelineUsecase

from src.infrastructure.data_drivers.data_extractor_driver import DataExtractorDriver
from src.infrastructure.data_drivers.data_transformer_driver import DataTransformerDriver
from src.infrastructure.data_drivers.data_loader_driver import DataLoaderDriver
from src.infrastructure.loggers.logger_driver import LoggerDriver

def main():
  logger_driver = LoggerDriver()
  
  data_extractor_driver = DataExtractorDriver(logger_driver)
  data_transformer_driver = DataTransformerDriver(logger_driver)
  data_loader_driver = DataLoaderDriver(logger_driver)
  
  extract_data_usecase = ExtractDataRawUsecase(
    data_extractor_driver,
    logger_driver)
  
  transform_data_usecase = TransformDataUsecase(
    data_transformer_driver,
    logger_driver)
  
  dump_data_usecase = DumpDataUsecase(
    data_loader_driver,
    logger_driver)
  
  data_pipeline_usecase = DataPipelineUsecase(
    extract_data_usecase,
    transform_data_usecase,
    dump_data_usecase,
    logger_driver)
  
  result = data_pipeline_usecase.extract_data_pipeline()
  result = data_pipeline_usecase.transform_data_pipeline(result)
  
  print(result)

if __name__ == "__main__":
  main()