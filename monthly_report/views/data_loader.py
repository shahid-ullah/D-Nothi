# file uploading, processing

# later this will be used for data upload handling, cleaning, pruning etc.

FILE_NAME = 'dataset-2.csv'
root = ''


# loading data from the uploads folder

def data_load():
    print(FILE_NAME)
    import pandas as pd
    try:
        excel_ds = root + FILE_NAME  # read from file
        subjects = pd.read_csv(excel_ds, encoding='utf-8')
    except:
        print('File error')
        subjects = 'File error, Re-Upload the File'

    return subjects

def data_load_with_age():
    FILE_NAME = 'subjects_age_8mb.csv'
    print(FILE_NAME)
    import pandas as pd

    try:
        excel_ds = root + FILE_NAME  # read from file
        subjects = pd.read_csv(excel_ds, encoding='utf-8')
    except:
        print('File error')
        subjects = 'File error, Re-Upload the File'

    return subjects

def data_load_dashboard():
    FILE_NAME = 'patient-data_now.csv'
    print(FILE_NAME)
    import pandas as pd

    try:
        excel_ds = root + FILE_NAME  # read from file
        subjects = pd.read_csv(excel_ds, encoding='utf-8')
    except:
        print('File error')
        subjects = 'File error, Re-Upload the File'

    return subjects

# load the final csv file provided by niton vai, with updated vaccination details
# I added age, year column
def data_load_consultation():
    FILE_NAME = 'consultation_data.csv'
    print(FILE_NAME)
    import pandas as pd

    try:
        excel_ds = root + FILE_NAME  # read from file
        subjects = pd.read_csv(excel_ds, encoding='utf-8')
    except:
        print('File error')
        subjects = 'File error, Re-Upload the File'

    return subjects