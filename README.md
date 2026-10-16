# Sistema de Controle de EPI

## Descrição
Projeto desenvolvido em Django para realizar o controle de Equipamentos de Proteção Individual (EPI), permitindo cadastrar colaboradores e equipamentos, registrar empréstimos e acompanhar as situações dos equipamentos.

## Funcionalidades
- Cadastro, consulta, edição e exclusão de colaboradores.
- Cadastro e gerenciamento de equipamentos.
- Registro e acompanhamento de empréstimos de EPI.
- Consulta de empréstimos e filtros por informações.
- Controle de status dos equipamentos.

## Tecnologias utilizadas
- Python
- Django
- SQLite
- HTML e CSS
- Git e GitHub

## Como executar o projeto

1. Instale o Python.
2. Clone o repositório:

   ```bash
   git clone https://github.com/suellenbianca/projeto-epi.git
   ```

3. Entre na pasta do projeto:

   ```bash
   cd projeto-epi
   ```

4. Crie um ambiente virtual:

   ```bash
   python -m venv venv
   ```

5. Ative o ambiente virtual no Windows:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

6. Instale o Django:

   ```bash
   python -m pip install django
   ```

7. Crie as tabelas do banco de dados:

   ```bash
   python manage.py migrate
   ```

8. Inicie o servidor:

   ```bash
   python manage.py runserver
   ```

9. Acesse no navegador:

   http://127.0.0.1:8000/

## Observação
O banco de dados local não é enviado ao GitHub. As tabelas podem ser criadas por meio das migrações do Django.
