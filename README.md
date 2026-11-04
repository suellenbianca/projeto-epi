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

## Autenticação e controle de acesso

O sistema possui autenticação de usuários e controle de permissões para garantir que cada pessoa tenha acesso somente às funcionalidades autorizadas.

### Funcionalidades de autenticação

- Tela de login para acesso ao sistema.
- Autenticação obrigatória para acessar as páginas internas.
- Funcionalidade de logout para encerrar a sessão.
- Gerenciamento de usuários pelo Django Admin.
- Criação de grupos de usuários com diferentes níveis de permissões.
- Controle de acesso às funcionalidades de cadastro, consulta, edição e exclusão.

### Gerenciamento de grupos e permissões

A administração dos usuários e grupos é realizada pelo painel administrativo do Django, acessado pelo endereço:

http://127.0.0.1:8000/admin/


Pelo Django Admin, é possível criar grupos e definir permissões específicas para cada modelo do sistema.

O projeto possui os seguintes grupos configurados:

**Grupo Consulta**

Possui permissão somente para visualizar os registros de:

- Colaboradores;
- Equipamentos;
- Empréstimos.

Não possui permissão para adicionar, editar ou excluir registros.

**Grupo Gestor**

Possui permissões para realizar todas as operações nos modelos:

- Colaboradores;
- Equipamentos;
- Empréstimos.

Pode visualizar, adicionar, editar e excluir registros.

**Administrador**

O superusuário possui acesso administrativo completo, podendo gerenciar usuários, grupos e permissões pelo Django Admin.

### Controle de permissões

O controle de acesso é realizado em duas partes:

- **Backend:** utilização dos decoradores `login_required` e `permission_required` nas views do Django, impedindo que usuários sem autorização executem operações restritas.
- **Templates:** utilização das permissões do Django para controlar a exibição dos botões de cadastrar, editar e excluir conforme o grupo do usuário.

Quando um usuário autenticado tenta acessar uma funcionalidade sem possuir a permissão necessária, o sistema bloqueia a operação e apresenta o erro `403 Forbidden`.

Usuários que não estão autenticados são redirecionados para a tela de login ao tentar acessar páginas internas.

### Testes de autenticação e permissões

Foram realizados testes com usuários vinculados aos grupos Consulta e Gestor.

Os testes confirmaram que:

- Usuários não autenticados são redirecionados para a tela de login.
- Usuários do grupo Consulta conseguem visualizar os registros, mas não podem cadastrar, editar ou excluir.
- Usuários do grupo Gestor conseguem visualizar, cadastrar, editar e excluir registros.
- O acesso direto a funcionalidades sem permissão é bloqueado pelo Django.

Dessa forma, o sistema utiliza autenticação e autorização para proteger as informações e controlar as operações de acordo com as permissões de cada grupo.

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


git clone https://github.com/suellenbianca/projeto-epi.git
cd projeto-epi


### 2. Criar um ambiente virtual


python -m venv venv


### 3. Ativar o ambiente virtual no Windows

No PowerShell:


.\venv\Scripts\Activate.ps1


### 4. Instalar as dependências


python -m pip install -r requirements.txt


### 5. Criar as tabelas do banco de dados


python manage.py migrate


### 6. Iniciar o servidor


python manage.py runserver


### 7. Acessar o sistema

Abra o navegador e acesse:

http://127.0.0.1:8000/

## Como executar com Docker

Os comandos a seguir devem ser executados no PowerShell, dentro da pasta do projeto. Antes de começar, confirme que o Docker Desktop está aberto e em execução.

### 1. Construir a imagem


docker build --load -t projeto-epi .


### 2. Criar a pasta de dados


New-Item -ItemType Directory -Force dados


Se já existir uma pasta `dados` com o arquivo do banco atual, não a apague nem substitua o arquivo.

### 3. Criar e iniciar o contêiner

Se ainda não existir um contêiner chamado `epi-sistema`, execute:


docker run -d --name epi-sistema -p 8000:8000 -v "${PWD}\dados:/app/dados" projeto-epi


### 4. Aplicar as migrações


docker exec epi-sistema python manage.py migrate


### 5. Acessar o sistema

Abra o navegador e acesse:

http://127.0.0.1:8000/

### Iniciar ou parar o contêiner

Para iniciar um contêiner que já existe:


docker start epi-sistema


Para parar o contêiner:


docker stop epi-sistema


Não é necessário criar outro contêiner toda vez que quiser usar o sistema. Se o contêiner `epi-sistema` já existir, use `docker start epi-sistema`.

## Banco de dados e recuperação dos registros

O projeto utiliza SQLite. No ambiente Docker configurado para este projeto, o arquivo do banco de dados fica em:


dados/db.sqlite3


A pasta `dados` do computador é vinculada ao caminho `/app/dados` dentro do contêiner. Assim, os dados permanecem no computador quando o contêiner é parado ou removido, desde que o arquivo local seja preservado.

### Fazer backup do banco de dados

Antes de fazer alterações importantes, pare o contêiner para evitar cópias enquanto o banco está sendo utilizado:


docker stop epi-sistema


Faça uma cópia do arquivo `dados\db.sqlite3` para um local seguro. Depois, você pode iniciar o contêiner novamente:


docker start epi-sistema


### Recuperar colaboradores, equipamentos e empréstimos

Para recuperar os registros existentes, é necessário ter uma cópia do arquivo `db.sqlite3` que contenha esses dados.

1. Pare o contêiner, se estiver em execução:

   
   docker stop epi-sistema
   

2. Faça uma cópia de segurança do arquivo atual `dados\db.sqlite3`, se ele existir.

3. Coloque o arquivo de banco de dados que deseja recuperar dentro da pasta `dados`, com o nome `db.sqlite3`.

4. Inicie o contêiner:

   
   docker start epi-sistema
   

5. Acesse http://127.0.0.1:8000/ e confira os registros.

**Importante:** as migrações do Django criam ou atualizam a estrutura das tabelas, mas não recuperam os registros antigos. Para restaurar os dados, é necessário utilizar o arquivo de banco de dados que os contém.

## GitHub e proteção dos dados

O código-fonte do projeto está disponível em:

https://github.com/suellenbianca/projeto-epi

O banco de dados local não deve ser publicado no GitHub, pois pode conter informações pessoais, como CPF, telefone e e-mail. O arquivo `db.sqlite3` deve permanecer fora do repositório. Para demonstrações ou avaliações, prefira utilizar dados fictícios ou compartilhar uma cópia do banco somente por um meio autorizado e seguro.

## Autor

Projeto acadêmico desenvolvido para fins de aprendizagem em desenvolvimento de sistemas.

