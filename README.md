# richard_bot
A minimal implementation of a discord bot for a private discord server.

The bot is written in python3 using discord.py. If you're interested in making a
bot of your own a good place to start would be the official documentation [here](https://discordpy.readthedocs.io).
Additionally, I also personally recommend watching [this](https://www.youtube.com/playlist?list=PLW3GfRiBCHOhfVoiDZpSz8SM_HybXRPzZ) video tutorial series.

## Prerequisites
- richard_bot requires the python library **discord.py** to run. You can install this using pip
```
pip install discord.py
```
- You will need access to your bot's token. More information on that [here](https://discord.com/developers/docs/intro).

## Implementation details
- **main.py** searches for the bot token in a module called **secrets.py**
  this file should contain a variable called TOKEN in the format:
  ```
  TOKEN = 'Your token goes here'
  ```
  This file is hidden according to the project's **.gitignore**. for security
  reasons. Before running **main.py** make sure to copy **bot_token.py**
  from **/default_token/**, replace the empty string in it with your token,
  rename it to **secrets.py** and move it to the same directory as **main.py**.

## Notes
- Since this bot was designed for personal use, random features may be added
  or removed as needed without discretion.

## License
- richard_bot uses the MIT License which you can read [here](LICENSE).
