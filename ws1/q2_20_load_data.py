import dlt
import rich
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.paginators import PageNumberPaginator


@dlt.resource(name="rides")
def ny_taxi():
    client = RESTClient(
        base_url="https://us-central1-dlthub-analytics.cloudfunctions.net/",
        paginator=PageNumberPaginator(
            base_page=1,
            total_path=None,
        ),
    )
    for page in client.paginate("data_engineering_zoomcamp_api"):
        yield page


pipeline = dlt.pipeline(
    pipeline_name="ny_taxi_pipeline",
    destination="duckdb",
    dataset_name="ny_taxi_data",
)

if __name__ == '__main__':
    load_info = pipeline.run(ny_taxi)
    rich.print(load_info)
    rich.print(
        '\n\nSingle item from new dataset:',
        pipeline.dataset(dataset_type="default").rides.fetchone(),
    )
