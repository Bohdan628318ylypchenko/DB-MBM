from requests import Session
from requests.adapters import HTTPAdapter, Retry
import os
import alembic.config
from loguru import logger
from time import sleep


s = Session()
r = Retry(total=5, backoff_factor=0.1,)
s.mount("http://", HTTPAdapter(max_retries=r))


def funnel_scheme(args) -> None:
    """
    Executes db migration to prepare db for funnel execution.
    :param args: funnel migration revision as tuple element.
    """
    funnel_revision = args[0]
    alembic_args = ['upgrade', funnel_revision]
    alembic.config.main(argv=alembic_args)


def funnel_execute(args) -> None:
    """
    Calls funnel by http.
    :param args: funnel execution start endpoint url as tuple element.
    :raise: Exception when funnel response is not 201
    """
    funnel_url = args[0]
    response = s.post(funnel_url)
    if response.status_code != 201:
        raise Exception(f"invalid funnel response = {response.text}")


def service_worker_scheme(args) -> None:
    """
    Executes db migration to prepare db for service worker execution.
    :param args: service worker migration revision as tuple element.
    """
    service_worker_revision = args[0]
    alembic_args = ['upgrade', service_worker_revision]
    alembic.config.main(argv=alembic_args)


def service_worker_execute(args) -> None:
    """
    Calls service worker by http.
    :param args: service worker execution start endpoint url as tuple element.
    """
    service_worker_url = args[0]
    response = s.post(service_worker_url)
    if response.status_code != 201:
        raise Exception(f"invalid service worker response = {response.text}")


def crud_scheme(args) -> None:
    """
    Executes db migration to prepare db for crud execution.
    :param args: crud migration revision as tuple element.
    """
    crud_revision = args[0]
    alembic_args = ['upgrade', crud_revision]
    alembic.config.main(argv=alembic_args)


def crud(args) -> None:
    """
    Calls crud health check to ensure crud is working.
    :param args: crud health check url as tuple element.
    """
    crud_health_check_url = args[0]
    response = s.get(crud_health_check_url, timeout=10)
    if response.status_code != 200:
        raise Exception(f"invalid consumer health check response = {response.text}")


def main():
    """
    Deploys db-mbm project.
    Deployment stages:
    funnel -> service worker
    """
    deploy_fail_sleep = int(os.environ["DEPLOY_FAIL_SLEEP"])

    # deploy targets declaration
    targets = (
        ("funnel-scheme", funnel_scheme, ("bea454ec661d",)),
        ("funnel", funnel_execute, (os.environ["FUNNEL_URL"],)),
        ("service-worker-scheme", service_worker_scheme, ("fc3d481135d4",)),
        ("service-worker", service_worker_execute, (os.environ["SERVICE_WORKER_URL"],)),
        ("crud-scheme", crud_scheme, ("9e9fb73a0645",)),
        ("crud", crud, (os.environ["CRUD_URL"],))
    )

    # run deployment
    for target in targets:
        name, deploy, args = target
        while True:
            logger.info(f"{name} deployment attempt")
            try:
                deploy(args)
                logger.info(f"{name} deployment successful")
                break
            except Exception as e:
                logger.error(f"{name} deployment failed, retry in {deploy_fail_sleep} seconds, exception: {e}")
                sleep(deploy_fail_sleep)


if __name__ == '__main__':
    main()
