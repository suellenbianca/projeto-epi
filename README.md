# Sistema de Controle de EPI

## Descrição

Projeto desenvolvido em Django para realizar o controle de Equipamentos de Proteção Individual (EPI). O sistema permite cadastrar e gerenciar colaboradores e equipamentos, registrar empréstimos e acompanhar a situação dos equipamentos.

## Funcionalidades

- Cadastro, consulta, edição e exclusão de colaboradores.
- Pesquisa de colaboradores pelo nome.
- Cadastro e gerenciamento de equipamentos.
- Registro e acompanhamento de empréstimos de EPI.
- Consulta de empréstimos e filtros por informações.
- Controle da situação dos equipamentos.
- Armazenamento dos dados em banco de dados SQLite.

## Tecnologias utilizadas

- Python
- Django
- SQLite
- HTML e CSS
- Git e GitHub
- Docker

## Pré-requisitos

Para executar o projeto localmente, instale Python e Git.

Para executar com Docker, instale também o Docker Desktop e mantenha-o em execução.

## Como executar o projeto localmente

### 1. Clonar o repositório

```bash
git clone https://github.com/suellenbianca/projeto-epi.git
cd projeto-epi
```

### 2. Criar um ambiente virtual

```bash
python -m venv venv
```

### 3. Ativar o ambiente virtual no Windows

No PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

### 5. Criar as tabelas do banco de dados

```bash
python manage.py migrate
```

### 6. Iniciar o servidor

```bash
python manage.py runserver
```

### 7. Acessar o sistema

Abra o navegador e acesse:

http://127.0.0.1:8000/

## Como executar com Docker

Os comandos a seguir devem ser executados no PowerShell, dentro da pasta do projeto. Antes de começar, confirme que o Docker Desktop está aberto e em execução.

### 1. Construir a imagem

```powershell
docker build --load -t projeto-epi .
```

### 2. Criar a pasta de dados

```powershell
New-Item -ItemType Directory -Force dados
```

Se já existir uma pasta `dados` com o arquivo do banco atual, não a apague nem substitua o arquivo.

### 3. Criar e iniciar o contêiner

Se ainda não existir um contêiner chamado `epi-sistema`, execute:

```powershell
docker run -d --name epi-sistema -p 8000:8000 -v "${PWD}\dados:/app/dados" projeto-epi
```

### 4. Aplicar as migrações

```powershell
docker exec epi-sistema python manage.py migrate
```

### 5. Acessar o sistema

Abra o navegador e acesse:

http://127.0.0.1:8000/

### Iniciar ou parar o contêiner

Para iniciar um contêiner que já existe:

```powershell
docker start epi-sistema
```

Para parar o contêiner:

```powershell
docker stop epi-sistema
```

Não é necessário criar outro contêiner toda vez que quiser usar o sistema. Se o contêiner `epi-sistema` já existir, use `docker start epi-sistema`.

## Banco de dados e recuperação dos registros

O projeto utiliza SQLite. No ambiente Docker configurado para este projeto, o arquivo do banco de dados fica em:

```text
dados/db.sqlite3
```

A pasta `dados` do computador é vinculada ao caminho `/app/dados` dentro do contêiner. Assim, os dados permanecem no computador quando o contêiner é parado ou removido, desde que o arquivo local seja preservado.

### Fazer backup do banco de dados

Antes de fazer alterações importantes, pare o contêiner para evitar cópias enquanto o banco está sendo utilizado:

```powershell
docker stop epi-sistema
```

Faça uma cópia do arquivo `dados\db.sqlite3` para um local seguro. Depois, você pode iniciar o contêiner novamente:

```powershell
docker start epi-sistema
```

### Recuperar colaboradores, equipamentos e empréstimos

Para recuperar os registros existentes, é necessário ter uma cópia do arquivo `db.sqlite3` que contenha esses dados.

1. Pare o contêiner, se estiver em execução:

   ```powershell
   docker stop epi-sistema
   ```

2. Faça uma cópia de segurança do arquivo atual `dados\db.sqlite3`, se ele existir.

3. Coloque o arquivo de banco de dados que deseja recuperar dentro da pasta `dados`, com o nome `db.sqlite3`.

4. Inicie o contêiner:

   ```powershell
   docker start epi-sistema
   ```

5. Acesse http://127.0.0.1:8000/ e confira os registros.

**Importante:** as migrações do Django criam ou atualizam a estrutura das tabelas, mas não recuperam os registros antigos. Para restaurar os dados, é necessário utilizar o arquivo de banco de dados que os contém.

## GitHub e proteção dos dados

O código-fonte do projeto está disponível em:

https://github.com/suellenbianca/projeto-epi

O banco de dados local não deve ser publicado no GitHub, pois pode conter informações pessoais, como CPF, telefone e e-mail. O arquivo `db.sqlite3` deve permanecer fora do repositório. Para demonstrações ou avaliações, prefira utilizar dados fictícios ou compartilhar uma cópia do banco somente por um meio autorizado e seguro.

## Autor

Projeto acadêmico desenvolvido para fins de aprendizagem em desenvolvimento de sistemas.

