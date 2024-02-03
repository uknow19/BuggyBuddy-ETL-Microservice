import requests
import json
import concurrent.futures
from urllib.parse import urlencode
from typing import Any, Dict, Optional

from core.ports.data_extractor_port import DataExtractorPort
from core.models.raw_data_model import RawDataModel

import pandas as pd
import numpy as np

from core.types.common_types import ArrayLike, MatrixLike

class DataExtractorDriver(DataExtractorPort):
  def __init__(self) -> None:
    pass
  
  def fetch_data(url: str, params=None):
    try:
      response = requests.get(url, params=params)
      if (response.status_code == 200):
        return response.json()
      
      print(f"Error response with status code: {response.status_code}")
    except Exception as error:
      print(f'Failed to fetch data: {error}')
      
  def urls_builder(base_url: str, n_fetch: int, limit: int, **kwargs) -> str:
    urls = []
    for i in range(n_fetch):
      param = {
        'offset': i * limit,
        'limit': limit,
        **kwargs,
      }
      
      full_url = base_url + '?' + urlencode(param)
      urls.append(full_url)

    return urls
  
  def get_data_from_source(self, fields: Dict[str, Any], excludes: Optional[ArrayLike] = None) -> MatrixLike:
    base_url = 'https://bugzilla.mozilla.org/rest/bug'
    n_fetch = 50
    limit = 5000

    urls = self.urls_builder(base_url, n_fetch, limit, **fields)
    response_data = []

    max_workers = 50
    with concurrent.futures.ThreadPoolExecutor(max_workers) as executor:
      response_data = list(executor.map(self.fetch_data, urls))
      
    response_data = [item['bugs'] for item in response_data]
    response_data = [item for sublist in response_data for item in sublist]
    
    data = pd.DataFrame(response_data)
    data = data.set_index('id')
    
    if excludes:
      data = data.drop(columns=excludes)
    
    return data
  
  def format_raw_data(self, data: MatrixLike, excludes: Optional[ArrayLike] = None) -> MatrixLike:
    model_columns = list[RawDataModel.__annotations__.keys()]
    data_columns = ['id', 'type', 'status', 'product', 'component', 'platform', 'summary', 'description', 'resolution', 'severity', 'priority', 'duplicates']
    
    if excludes:
      data_columns = [col for col in data_columns if data not in excludes]
    
    column_mapper = {key: value for key, value in zip(data_columns, model_columns)}
    data = data.rename(columns=column_mapper)
    
    return data
    