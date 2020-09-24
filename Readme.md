# Vorkurs Discordbot

`discordbot.py` is the main script file for the bot.
The data is stored in a sqlite3 database `data.db` in `./storage/`.
The material git repository is needed in `./storage/materials/`.
Keys are placed in `./modules/credPrivate.py`.

### Tools needed

* python 3.8, 
* texlive-full, 
* access to the material repository, 
* selenium chrome

### Docker adaptation

To access the repository ssh keys are needed.
They are placed in `./key/` as `id_ed25519` and `id_ed25519.pub` for the docker.

### Keys

| Key | meaning |
| --- | --- |
| socialkey | key to access social team commands |
| BotToken | token of the discord bot |
| imgbbToken | imgBB token to upload images |
| miroOAuth| authentification for new miro boards |