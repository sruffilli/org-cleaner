import click
import logging
from google.cloud import asset
from modules import firewall_policies, log_sinks, org_policies

logging.basicConfig(format='[%(levelname)s] - %(asctime)s - %(message)s')
logging.root.setLevel(logging.INFO)


@click.command()
@click.argument("organization_id", type=str, required=True)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Perform a dry-run without actual deletions.")
@click.option(
    '--exclude-log-sinks',
    help="Log sinks to exclude in '{organizations,folders}/{id}/sinks/{sink_name}' format, comma separated."
)
#organizations/100893780470/sinks/sst_multiorg_activity_sink
@click.option(
    "--only-fwpolicies", is_flag=True, help="Only delete firewall policies.")
@click.option("--only-logsinks", is_flag=True, help="Only delete log sinks.")
@click.option(
    "--only-orgpolicies",
    is_flag=True,
    help="Only delete organization policies")
def main(organization_id, exclude_log_sinks, dry_run, only_orgpolicies,
         only_fwpolicies, only_logsinks):
  logging.info("Starting")
  delete_all = not any([only_orgpolicies, only_logsinks, only_fwpolicies])
  cai_client = asset.AssetServiceClient()

  if delete_all or only_orgpolicies:
    org_policies.delete(cai_client, organization_id, dry_run)

  if delete_all or only_fwpolicies:
    firewall_policies.delete(cai_client, organization_id, dry_run)

  if delete_all or only_logsinks:
    log_sinks.delete(cai_client, organization_id, exclude_log_sinks, dry_run)


if __name__ == "__main__":
  main()
