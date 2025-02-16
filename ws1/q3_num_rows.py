import rich
from q2_20_load_data import pipeline


if __name__ == '__main__':
    df = pipeline.dataset(dataset_type="default").rides
    rich.print('Rides dataset has', len(df.fetchall()), 'rows')
