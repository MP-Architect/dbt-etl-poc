from pathlib import Path

from dagster import Definitions
from dagster_dbt import DbtCliResource

from .assets import DBT_PROJECT_DIR, etl_job, etl_schedule, my_dbt_assets

defs = Definitions(
    assets=[my_dbt_assets],
    schedules=[etl_schedule],
    jobs=[etl_job],
    resources={
        "dbt": DbtCliResource(  # ← this was missing
            project_dir=str(DBT_PROJECT_DIR),
            profiles_dir=str(DBT_PROJECT_DIR),
        )
    },
)
