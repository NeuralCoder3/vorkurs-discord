
guesses=dict()
currentGame="None"
guesses[currentGame]=dict()

def nextGame(message,args):
    global currentGame
    if len(args)<1:
        return message.channel.send(f"wrong syntax")
    name=args[0]
    guesses[name]=dict()
    currentGame=name

def gameAnswers(game):
    text=""
    answers=guesses[game]
    text+="{"+game+"}\n"
    for channel,answer in answers.items():
        _,channelName=channel
        text+=f"  {channelName} -> {answer}\n"
    return text

def showGame(message,args):
    name="all" if len(args)<1 else args[0]
    text=""
    if name=="all":
        for game,_ in guesses.items():
            text+=gameAnswers(game)
    else:
        text=gameAnswers(name)
    return message.channel.send(text)


def guess(message,args):
    if len(args)<1:
        return message.channel.send(f"wrong syntax: guess answer")
    id=message.channel.id
    name=message.channel.name
    answer=args[0]
    resultText="Answer updated." if (id,name) in guesses[currentGame] else "Answer sent."
    guesses[currentGame][(id,name)]=answer
    return message.channel.send(resultText)