## To generate secret key just run this -

```bash
     openssl rand -hex 32
```
## To make migrations 
### in alembic.ini point actual database url
for postgresql local it is
#### DATABASE_URL: "postgresql://postgres:postgres@localhost:5432/postgres"

```bash 
alembic init migrations
```
```bash
alembic revision --autogenerate
```
```bash
alembic upgrade head
```
