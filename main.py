import logging
import os
from pathlib import Path

from dotenv import load_dotenv
import pandas as pd

from validators import validate


load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(filename='logs/logs.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
FILEPATH = os.getenv("FILEPATH")


df = pd.read_json(FILEPATH)
df = validate(df)

# Drop redundant indexes
df.index = df.id
df.drop('id', axis=1, inplace=True)

# the final pivot table
result = df.groupby('category') \
    .agg({"price": "sum", "owner": "count"}) \
    .rename(columns={"owner": "amount", "price": "total_sum"})
print(result)
answer_1 = dict(result.total_sum.apply(int))
print(answer_1)
answer_2 = dict(result.amount.apply(int))
print(answer_2)

logger.info(f"{answer_1}")
logger.info(f"{answer_2}")
