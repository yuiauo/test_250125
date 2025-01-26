import pandas as pd

from app_logger import logger


def validate_unique(df: pd.DataFrame) -> bool:
    """ Checks for repeating data """
    return len(df) == df.id.nunique()


def validate_not_null(df: pd.DataFrame) -> bool:
    """ Checks for NaN values """
    return df.isnull().sum().sum() == 0


def validate_price(df: pd.DataFrame) -> bool:
    """ Checks for positive price """
    return df.price.min() > 0


def validate(df: pd.DataFrame) -> pd.DataFrame:
    """ Validates and optionally cleans data """
    if not validate_unique(df):
        # I guess the `id` column supposed to be unique.
        # So having duplicates means having same ids.
        # Either we can use .drop_duplicates(subset=<scope of repeatables>)
        df = df[~df.id.duplicated()]
        logger.warning(f"Data duplicates have been removed")
    if not validate_not_null(df):
        df.dropna(inplace=True)
        logger.warning(f"Empty data has been removed")
    if not validate_price(df):
        df = df[df.price > 0]
        logger.warning(f"Non-positive prices have been removed")
    return df