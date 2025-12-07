"""Safe insert: reuse existing `empresa` if present, otherwise create one,
then insert an admin `usuario` only if the email is not present.

Usage: set `SUPABASE_URL` and `SUPABASE_KEY_SERVICE_ROLE` in the environment
and run this script with the project's Python.
"""
import os
import sys
import time
from supabase import create_client
from werkzeug.security import generate_password_hash


def main():
    url = os.environ.get('SUPABASE_URL')
    key = os.environ.get('SUPABASE_KEY_SERVICE_ROLE') or os.environ.get('SUPABASE_KEY_ANON')
    if not url or not key:
        print('ERROR: set SUPABASE_URL and SUPABASE_KEY_SERVICE_ROLE')
        return 2

    client = create_client(url, key)

    # Prefer lookup by a stable test cnpj; adjust if you use a different pattern
    test_cnpj = '00000000000000'

    try:
        resp = client.table('empresa').select('*').eq('cnpj', test_cnpj).limit(1).execute()
        if getattr(resp, 'error', None):
            print('empresa lookup error:', resp.error)
            return 1

        if resp.data:
            empresa = resp.data[0]
            print('Found existing empresa:', empresa)
            empresa_id = empresa['id']
        else:
            # create a unique nome to avoid unique constraint by name
            ts = int(time.time())
            nome = f'Empresa Teste Auto {ts}'
            cnpj = test_cnpj[:-3] + f"{ts % 1000:03d}"
            empresa_obj = {'nome': nome, 'cnpj': cnpj}
            print('Inserting new empresa:', empresa_obj)
            resp_i = client.table('empresa').insert(empresa_obj).execute()
            if getattr(resp_i, 'error', None):
                print('empresa insert error:', resp_i.error)
                return 1
            empresa_id = resp_i.data[0]['id']
            print('Inserted empresa id:', empresa_id)

        # prepare usuario
        ts = int(time.time())
        email = f'admin_auto_{empresa_id}_{ts}@example.com'

        # check if user email already exists
        resp_user = client.table('usuario').select('*').eq('email', email).limit(1).execute()
        if getattr(resp_user, 'error', None):
            print('usuario lookup error:', resp_user.error)
            return 1
        if resp_user.data:
            print('User already exists:', resp_user.data[0])
            return 0

        usuario = {
            'nome': 'Admin Auto',
            'email': email,
            'senha_hash': generate_password_hash('changeme123'),
            'id_empresa': empresa_id
        }
        print('Inserting usuario:', {'email': usuario['email'], 'id_empresa': usuario['id_empresa']})
        resp_u = client.table('usuario').insert(usuario).execute()
        if getattr(resp_u, 'error', None):
            print('usuario insert error:', resp_u.error)
            return 1

        print('Usuario inserted:', resp_u.data)
        return 0

    except Exception as e:
        print('Exception during safe insert:', str(e))
        return 1


if __name__ == '__main__':
    sys.exit(main())

