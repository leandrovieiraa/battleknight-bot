![img](https://gameforge.com/en-GB/infos/content/themes/gameforge/custom/img/gamecards/battleknight.jpeg)

# Battle Knight BOT

## Gameinfo

Website: https://br.battleknight.gameforge.com/

## Python

Version 3.8+

## Considerations

This is a simple version, where the player will do random missions on the first map (low level character < 5) and after doing the mission, the player will work randomly, varying the time and type of work.

This routine is executed in an infinite loop, where it'll wait for the mission and also the work time, don't worry if you run out of mission points, soon it will be regenerated.

The script doesn't check the player's health, so the player can go to missions with low HP.

Be `careful` when running this script, you may get blocked or banned out of this game, it's up to you.

## Setup and run

Install libs:

```bash
pip install -r requirements.txt
```

Rename `.env.sample` to `.env`, configure your credentials and now you can run the script:

```
python main.py
```


