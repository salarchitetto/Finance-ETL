from Banks.pnc import PNC
from Banks.vangaurd import Vanguard
from Banks.nelnet import Nelnet
from Banks.acorns import Acorns
from Banks.slavik import Slavik
from Plaid.plaid import Plaid
from configs import Configs

pnc_client = Plaid(Configs.creds_helper("PNC")["ACCESS_KEY"],
                   Configs.creds_helper("PLAID_API_KEYS")["CLIENT_ID"],
                   Configs.creds_helper("PLAID_API_KEYS")["SECRET"],
                   Configs.creds_helper("PLAID_API_KEYS")["PUBLIC_KEY"])

acorns_client = Plaid(Configs.creds_helper("ACORNS")["ACCESS_KEY"],
                      Configs.creds_helper("PLAID_API_KEYS")["CLIENT_ID"],
                      Configs.creds_helper("PLAID_API_KEYS")["SECRET"],
                      Configs.creds_helper("PLAID_API_KEYS")["PUBLIC_KEY"])

vanguard_client = Plaid(Configs.creds_helper("VANGUARD")["ACCESS_KEY"],
                        Configs.creds_helper("PLAID_API_KEYS")["CLIENT_ID"],
                        Configs.creds_helper("PLAID_API_KEYS")["SECRET"],
                        Configs.creds_helper("PLAID_API_KEYS")["PUBLIC_KEY"])

slavic_client = Plaid(Configs.creds_helper("SLAVIC")["ACCESS_KEY"],
                      Configs.creds_helper("PLAID_API_KEYS")["CLIENT_ID"],
                      Configs.creds_helper("PLAID_API_KEYS")["SECRET"],
                      Configs.creds_helper("PLAID_API_KEYS")["PUBLIC_KEY"])

nelnet_client = Plaid(Configs.creds_helper("NELNET")["ACCESS_KEY"],
                      Configs.creds_helper("PLAID_API_KEYS")["CLIENT_ID"],
                      Configs.creds_helper("PLAID_API_KEYS")["SECRET"],
                      Configs.creds_helper("PLAID_API_KEYS")["PUBLIC_KEY"])

if __name__ == '__main__':

    #initilize classes
    pnc = PNC(pnc_client)
    acorns = Acorns(acorns_client)
    vangaurd = Vanguard(vanguard_client)
    slavic = Slavik(slavic_client)
    nelnet = Nelnet(nelnet_client)

    #Runners
    pnc.run_pnc_module()
    acorns.run_acorns_module()
    vangaurd.run_vanguard_module()
    slavic.run_slavik_module()
    nelnet.run_nelnet_module()
