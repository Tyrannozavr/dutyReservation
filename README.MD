# This project is created to make ability lots of users reserve some dates at the same time.


## This project  can work just with web authentication and by telegram webapp.

## To run proxy use one of these commands 

```bash
     ngrok http 80
```

```bash
    loclx tunnel http --to localhost:80
```
```bash
    lt --port 80
```

### if you want to skip manual authentication, make proxy (or host it on real server) and pass address of your application to BotFather. 
if you send link like https://<your_domain>/auth/telegram/ it will be more easy to authenticate user automatically

In backend/.env you have to set TELEGRAM_BOT_TOKEN (you can take it from BotFather) and SECRET_KEY (just generate you own for security)