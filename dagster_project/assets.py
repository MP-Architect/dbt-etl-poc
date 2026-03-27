from pathlib import Path

from dagster import AssetExecutionContext, ScheduleDefinition, define_asset_job
from dagster_dbt import DbtCliResource, DbtProject, dbt_assets

DBT_PROJECT_DIR = Path(__file__).parent.parent / "dbt_project"

dbt_project = DbtProject(
    project_dir=DBT_PROJECT_DIR,
    profiles_dir=DBT_PROJECT_DIR,
)


@dbt_assets(manifest=dbt_project.manifest_path)
def my_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(
        ["run", "--profiles-dir", str(DBT_PROJECT_DIR)], context=context
    ).stream()
    yield from dbt.cli(
        ["test", "--profiles-dir", str(DBT_PROJECT_DIR)], context=context
    ).stream()


etl_job = define_asset_job("etl_job", selection="*")

etl_schedule = ScheduleDefinition(
    job=etl_job,
    cron_schedule="0 * * * *",
    name="hourly_etl",
)
