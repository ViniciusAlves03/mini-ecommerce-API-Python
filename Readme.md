# API Mini E-commerce com Flask e SQLAlchemy
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![SQL Server](https://img.shields.io/badge/SQL%20Server-CC2927?style=for-the-badge&logo=microsoftsqlserver&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=jsonwebtokens&logoColor=white)
![Swagger](https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)

Esta é uma API RESTful completa para um sistema de mini e-commerce, construída com Python, Flask e SQLAlchemy. O projeto inclui funcionalidades essenciais como autenticação de usuários e lojas, gerenciamento de produtos e um sistema de carrinho de compras.

A autenticação é gerenciada via JSON Web Tokens (JWT) e a API é documentada usando Swagger.

## Funcionalidades Principais

* **Autenticação JWT**: Sistema de login e registro separado para `Usuários` (clientes) e `Lojas` (vendedores).
* **CRUD de Usuários**: Operações completas para criar, ler, atualizar e deletar usuários.
* **CRUD de Lojas**: Operações completas para criar, ler, atualizar e deletar lojas.
* **Gerenciamento de Produtos**: Lojas autenticadas podem criar, atualizar e deletar seus próprios produtos.
* **Sistema de Carrinho**: Usuários autenticados podem adicionar produtos ao carrinho, ver o carrinho, atualizar quantidades e "comprar" (limpando o carrinho e atualizando o estoque).
* **Documentação Swagger**: Todos os endpoints são documentados e podem ser testados interativamente através da interface do Swagger UI.

## Tecnologias Utilizadas

* **Python 3.x**
* **Flask**: Micro-framework web para construir a API.
* **Flask-SQLAlchemy**: ORM para interação com o banco de dados.
* **PyJWT**: Para geração e verificação de tokens de autenticação.
* **Flask-Swagger-UI**: Para servir a documentação da API.
* **python-dotenv**: Para gerenciar variáveis de ambiente.

---

## Instalação e Execução

Siga os passos abaixo para configurar e executar o projeto localmente.

### 1. Pré-requisitos

* Python 3.8 ou superior
* Um banco de dados (o projeto está configurado para SQL Server, mas pode ser adaptado no `DATABASE_URI`)

### 2. Clone o Repositório

```bash
git clone https://github.com/ViniciusAlves03/mini-ecommerce-API-Python.git
cd mini-ecommerce-API-Python
```

### 3. Crie e Ative um Ambiente Virtual

```bash
python -m venv venv
.\venv\Scripts\activate
```

### 4. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 5. Configure as Variáveis de Ambiente
Copie o arquivo .env.example e substitua os valores de exemplo por seus valores reais
```bash
cp .env.example .env
```

### 6. Execute a Aplicação
Com as variáveis de ambiente configuradas e o ambiente virtual ativado, inicie o servidor
```bash
flask run
```

O servidor estará rodando em `http://127.0.0.1:5000`

O `db.create_all()` no `app.py` criará automaticamente as tabelas no banco de dados na primeira vez que o servidor for iniciado.

## Estrutura do Projeto

```sh
.
├── auth_jwt/       # Lógica de criação e verificação do JWT
├── config/         # Carrega as configurações das variáveis de ambiente
├── models/         # Definições das tabelas do SQLAlchemy (User, Store, Product, Cart)
├── routes/         # Blueprints do Flask com a lógica dos endpoints
├── static/         # Arquivo swagger.yaml da documentação
├── utils/          # Módulos utilitários
├── venv/           # Ambiente virtual (ignorado pelo Git)
├── .env            # Arquivo local com chaves (ignorado pelo Git)
├── .env.example    # Arquivo de exemplo para configuração
├── app.py          # Ponto de entrada da aplicação Flask
├── requirements.txt  # Lista de dependências Python
└── README.md       # Esse arquivo
```

## Documentação da API (Endpoints)

Abaixo está um resumo de todos os endpoints disponíveis na API, agrupados por recurso.

Para uma documentação interativa completa, com detalhes de `schemas`, `body` e para testar os endpoints, acesse a documentação do Swagger (após iniciar o servidor): `http://127.0.0.1:5000/api/docs`

### 👤 User (Usuários Clientes)

Rotas para registro, login e gerenciamento de contas de clientes.

| Método | Rota (Path) | Descrição
| :--- | :--- | :--- |
| `GET` | `/users` | Lista todos os usuários cadastrados. |
| `POST` | `/user` | Cria um novo usuário (registro). |
| `POST` | `/user/login` | Autentica um usuário e retorna um token JWT. |
| `GET` | `/user/{user_id}` | Obtém os dados de um usuário específico. |
| `PUT` | `/user/{user_id}` | Atualiza os dados de um usuário específico. |
| `DELETE` | `/user/{user_id}` | Deleta a conta de um usuário específico. |
---

### 🏪 Store (Lojas / Vendedores)

Rotas para registro, login e gerenciamento de contas de lojas.

| Método | Rota (Path) | Descrição |
| :--- | :--- | :--- |
| `GET` | `/stores` | Lista todas as lojas cadastradas. |
| `POST` | `/store` | Cria uma nova loja (registro). |
| `POST` | `/store/login` | Autentica uma loja e retorna um token JWT. |
| `GET` | `/store/{store_id}` | Obtém os dados de uma loja específica. |
| `PUT` | `/store/{store_id}` | Atualiza os dados de uma loja específica. |
| `DELETE` | `/store/{store_id}` | Deleta a conta de uma loja específica. |

### 📦 Product (Produtos)

Rotas para visualização e gerenciamento de produtos.

| Método | Rota (Path) | Descrição |
| :--- | :--- | :--- |
| `GET` | `/products` | Lista todos os produtos de todas as lojas. |
| `GET` | `/products/{product_name}` | Busca um produto pelo nome. |
| `POST` | `/store/{store_id}/products` | Cria um novo produto para uma loja. |
| `GET` | `/store/{store_id}/products/{product_id}` | Obtém um produto específico de uma loja. |
| `PUT` | `/store/{store_id}/products/{product_id}` | Atualiza um produto específico de uma loja. |
| `DELETE` | `/store/{store_id}/products/{product_id}` | Deleta um produto específico de uma loja. |

### 🛒 Cart (Carrinho de Compras do Usuário)

| Método | Rota (Path) | Descrição |
| :--- | :--- | :--- |
| `GET` | `/user/{user_id}/cart` | Lista todos os itens no carrinho do usuário. |
| `POST` | `/user/{user_id}/cart/add` | Adiciona um produto ao carrinho. |
| `PUT` | `/user/{user_id}/cart/update/{product_id}` | Atualiza a quantidade de um item no carrinho. |
| `DELETE` | `/user/{user_id}/cart/delete_item/{product_id}` | Remove um item específico do carrinho. |
| `DELETE` | `/user/{user_id}/cart/clear` | Remove todos os itens do carrinho. |
| `POST` | `/user/{user_id}/cart/buy_item/{product_id}` | "Compra" um item (remove do carrinho e atualiza estoque). |
| `POST` | `/user/{user_id}/cart/buy_all` | "Compra" todos os itens (limpa o carrinho e atualiza estoque). |

---

## 🧑‍💻 Autor <a id="autor"></a>

<p align="center">Desenvolvido por Vinícius Alves <strong><a href="https://github.com/ViniciusAlves03">(eu)</a></strong>.</p>

---

