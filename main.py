import os

from dotenv import load_dotenv
import pandas as pd

from app_logger import logger
from validators import validate


load_dotenv()
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

answer_1 = {cat: sum_ for cat, sum_ in result.total_sum.items()}
answer_2 = {cat: am for cat, am in result.amount.items()}

logger.info(f"{answer_1}")
logger.info(f"{answer_2}")
