import pandas as pd


def process_app_file(path: str) -> pd.DataFrame:
    """reads file, process data and keeps only numeric columns

    Args:
        path (str): path to file

    Returns:
        pd.DataFrame: processed data
    """
    # TODO: when nulls are detected - it must be filled
    df = pd.read_excel(path)
    # check for numeric columns, keep only them
    df = df.loc[:, [pd.to_numeric(df.loc[~df[c].isna(), c], errors='coerce').notnull().all() for c in df]].astype(float)
    return df


if __name__ == "__main__":
    path = r"C:\Users\danii\temporal\test.xlsx"
    process_app_file(path)
