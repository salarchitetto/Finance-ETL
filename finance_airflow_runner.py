from datetime import datetime, timedelta

from Banks.acorns import Acorns
from Banks.nelnet import Nelnet
from Banks.pnc import PNC
from Banks.slavik import Slavik
from Banks.vangaurd import Vanguard
from Plaid.plaid import Plaid
from airflow import DAG
from airflow.models import Variable
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner': 'SalArchitetto',
    'start_date': datetime(2021, 1, 12),
    'depends_on_past': False,
    'email_on_retry': False,
    'retry_delay': timedelta(minutes=5),
    'retries': 3,
    'catchup_by_default': False
}

dag = DAG('finance_ETL',
          default_args=default_args,
          description='Financials for my life',
          schedule_interval='0 9 * * *',
          catchup=False
          )

plaid_client_id = Variable.get("PLAID_CLIENT_ID")
plaid_secret = Variable.get("PLAID_SECRET")
plaid_public_key = Variable.get("PLAID_PUBLIC_KEY")

pnc_client = Plaid(Variable.get("PNC"), plaid_client_id, plaid_secret, plaid_public_key)
acorns_client = Plaid(Variable.get("ACORNS"), plaid_client_id, plaid_secret, plaid_public_key)
vanguard_client = Plaid(Variable.get("VANGUARD"), plaid_client_id, plaid_secret, plaid_public_key)
slavic_client = Plaid(Variable.get("SLAVIC"), plaid_client_id, plaid_secret, plaid_public_key)
nelnet_client = Plaid(Variable.get("NELNET"), plaid_client_id, plaid_secret, plaid_public_key)


def run_pnc():
    return PNC(pnc_client).run_pnc_module()


def run_acorns():
    return Acorns(acorns_client).run_acorns_module()


def run_vangaurd():
    return Vanguard(vanguard_client).run_vanguard_module()


def run_slavic():
    return Slavik(slavic_client).run_slavik_module()


def run_nelnet():
    return Nelnet(nelnet_client).run_nelnet_module()


starter = DummyOperator(task_id='startin_the_bot', dag=dag)

pnc = PythonOperator(
    task_id="pnc_runner",
    python_callable=run_pnc,
    dag=dag
)

acorns = PythonOperator(
    task_id="acorns_runner",
    python_callable=run_acorns,
    dag=dag
)

vanguard = PythonOperator(
    task_id="vanguard_runner",
    python_callable=run_vangaurd,
    dag=dag
)

slavic = PythonOperator(
    task_id="slavic_runner",
    python_callable=run_slavic,
    dag=dag
)

nelnet = PythonOperator(
    task_id="nelnet_runner",
    python_callable=run_nelnet,
    dag=dag
)

the_end = DummyOperator(task_id="killin_the_etl", dag=dag)

starter >> pnc >> acorns >> vanguard >> slavic >> nelnet >> the_end