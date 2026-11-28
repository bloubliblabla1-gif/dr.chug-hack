import requests as rq

FORM_ID = "1lvI_JuSAyCXbIzwONaAmXsJ_pOpDHfqormJGJnU1rog"

def log(string, form_id, entry_number, verbose=False):
    url = f'https://docs.google.com/forms/d/{form_id}/formResponse'
    data = {f'entry.{entry_number}': string}

    try:
        response = rq.post(url, data=data)
        if response.status_code in [200, 302]:
            if verbose: print('Logging success.')
        else:
            print('Logger: error, status code:', response.status_code)
    except rq.RequestException as e:
        print('Logger: error:', e)

log("TEST ENTRY", FORM_ID, "300694629", verbose=True)
