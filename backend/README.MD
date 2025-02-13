## To generate secret key just run this -

```bash
     openssl rand -hex 32
```
## To make migrations 
```bash
alembic revision --autogenerate
```
```bash
alembic upgrade head
```
