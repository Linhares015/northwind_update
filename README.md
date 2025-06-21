# northwind_update

Projeto para inserir dados simulados e garantir colunas extras no banco Northwind (PostgreSQL), usando SQLAlchemy e Faker.

---

## Objetivo

- Popular tabelas do banco Northwind com dados realistas para testes e desenvolvimento.
- Garantir que as tabelas tenham as colunas `id` (serial) e `updated_at` (timestamp).

---

## Pré-requisitos

- Python 3.8+
- Docker (para rodar o banco Northwind)
- PostgreSQL rodando na porta 5432

---

## Instalação e Configuração

1. **Suba o banco Northwind via Docker:**

   ```sh
   docker run --rm -it \
     -p 5432:5432 \
     --name postgres-northwind \
     bradymholt/postgres-northwind:latest
   ```

2. **Altere a senha do usuário:**

   ```sh
   docker exec -it postgres-northwind psql -U northwind
   ```

   No prompt do psql:
   ```sql
   ALTER USER northwind WITH PASSWORD 'sua_senha_segura';
   ```

3. **Instale as dependências Python:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Configure a conexão no arquivo `.env`:**

   ```
   DB_URL=postgresql://northwind:sua_senha_segura@localhost:5432/northwind
   ```

---

## Estrutura do Projeto

```
src/
  ├── alter_schema.py      # Garante colunas extras nas tabelas
  ├── db.py                # Conexão e metadata do banco
  ├── models.py            # Mapeamento das tabelas
  └── generators/
        ├── customer.py    # Geração de clientes fake
        ├── order.py       # Geração de pedidos fake
        └── dynamic.py     # Geração dinâmica para qualquer tabela
main.py                    # Script principal
.env                       # Configuração da string de conexão
```

---

## Como usar

1. **Execute o script principal:**

   ```sh
   python src/main.py
   ```

   - O script irá:
     - Garantir as colunas `id` e `updated_at` nas tabelas principais.
     - Inserir dados fake nas tabelas `customers` e `orders`.

2. **Personalize a quantidade de dados**
   Edite o arquivo `main.py` para mudar o número de registros inseridos.

---

## Geração de Dados

- Usa o [Faker](https://faker.readthedocs.io/) para gerar dados realistas em português.
- Respeita chaves primárias, estrangeiras e tipos de dados das tabelas.

---

## Observações

- O projeto pode ser facilmente adaptado para outras tabelas do Northwind.
- Para adicionar mais tabelas, edite o arquivo `src/models.py` e os scripts em `generators/`.

---

## Licença

Uso livre para fins acadêmicos e de desenvolvimento.