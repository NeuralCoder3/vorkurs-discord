# Vorkurs Discordbot


| File | Content |
| ---- | --- |
| discordbot.py | A bot to serve urls of warmup sheets |
| miro.py | uploads a warmup sheet pdf to miro |
| markdown.py | creates an online markdown document from a warmup tex file |
| util.py | upload and conversion functions |
| template.md | the general frame of markdown warum sheets |
| answer.md | the template for each exercise and answer text |
| cred.py | sensitive data |

## Cred.py

Fill in the fields in the style
`field = "Text"`

| Field | Content |
| ---- | --- |
| BotToken | a discord token of the bot |
| imgbbToken | imgbb token to upload images |
| exercisePdfPool | pre compiled pdf files for each exercise (cropped) |
| browser | executable path to the browser for selenium |
|  |  |
| profileDir | profile for selenium to keep login |
| boardUrl | url of the whiteboard to upload to |
| testSheet1Tex | tex code for the warmup sheet |
| testSheet1PDF | pdf file of the warmup sheet |

The last four fields are temporary for testing and are not needed in the final bot.