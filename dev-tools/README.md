Dev tools and scripts used for local development and testing.

- `insert_safe.py` — insert or reuse a test `empresa` and create an admin `usuario`.
- `test_supabase_connection.py` — quick connection check.
- `insert_empresa_and_usuario.py` — earlier insert script (kept for reference).

These scripts may require `SUPABASE_URL` and `SUPABASE_KEY_SERVICE_ROLE` set in
the environment. Do NOT commit or share service-role keys. Use `.env` and
`python-dotenv` for local development.
