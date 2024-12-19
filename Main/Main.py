file_path = "heart_disease_dataset.csv"


def open_file(file_path: str):
    """
    Open a CSV file and loads it into DataFrame.

    Args:
        file_path (string): Path to the CSV file that is to be opened.

    Returns:
        data(pd.DataFrame):Loaded CSV file.
        None: If no file was found.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print("File not found")
        return None

if __name__ == '__main__':
    pass