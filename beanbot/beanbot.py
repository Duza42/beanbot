import asyncio
import logging
import logging.config
import logging.handlers
import os
import shutil
import sys

import discord
import yaml

# Configuration File Locations
CONFIG_PATH = "config/"
SAMPLES_PATH = "samples/"
MAIN_CONFIG_FILE = "config.yaml"
LOGGING_CONFIG_FILE = "logging.yaml"

members =[]
gameMode = False

# Read data from YAML file
def read_yaml_file(filename):
    try:
        with open(filename) as yaml_file:
            data = yaml.safe_load(yaml_file)
            return data
    except IOError as error:
        if LOGGER is None:
            print(f"File error: {str(error)}")
        else:
            LOGGER.error(f"File error: {str(error)}")


# Write data to YAML file
def write_yaml_file(filename, data):
    try:
        with open(filename, 'w') as yaml_file:
            yaml_file.write(yaml.safe_dump(data))
    except IOError as error:
        if LOGGER is None:
            print(f"File error: {str(error)}")
        else:
            LOGGER.error(f"File error: {str(error)}")


# Initialize logging
def init_logging():
    global LOGGER
    if not os.path.isfile(CONFIG_PATH + LOGGING_CONFIG_FILE):
        print("Copying default logging config file...")
        try:
            shutil.copy2(SAMPLES_PATH + LOGGING_CONFIG_FILE, CONFIG_PATH)
        except IOError as error:
            print(f"Unable to copy default logging config file. {str(error)}")
    logging_config = read_yaml_file(CONFIG_PATH + LOGGING_CONFIG_FILE)

    log_path = os.path.dirname(logging_config['handlers']['file']['filename'])
    try:
        if not os.path.exists(log_path):
            os.makedirs(log_path)
    except IOError:
        print("Unable to create log folder")
    logging.config.dictConfig(logging_config)
    LOGGER = logging.getLogger("beanbot")
    LOGGER.debug("Logging initialized...")


# Initialize configuration
def init_config():
    global CONFIG
    LOGGER.debug("Reading configuration...")
    if not os.path.isfile(CONFIG_PATH + MAIN_CONFIG_FILE):
        LOGGER.info("Copying default config file...")
        try:
            shutil.copy2(SAMPLES_PATH + MAIN_CONFIG_FILE, CONFIG_PATH)
        except IOError as error:
            LOGGER.error(f"Unable to copy default config file. {str(error)}")
    CONFIG = read_yaml_file(CONFIG_PATH + MAIN_CONFIG_FILE)


class beanBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

    async def on_ready(self):
        print('{0.user} is go'.format(client))
        with open('config/BigBrainOfBeanBot.txt','r') as brain:
            filecontents = brain.readlines()

            for line in filecontents:

                members.append(line.split(","))

                st = members[-1][1]
                st = st[:-1]
                members[-1][1] = st
                
        print('Members gathered from the brain')
        for i in members:
            print(i)
        brain.close()

    async def on_message(self, message):
        if message.author == client.user:
            return

        if 'hello' in message.content:
            await message.channel.send('yoooo')

        if message.content.startswith('Hello'):
            await message.channel.send(f'Hello <@!{message.author}>')

        if message.content.startswith('HELLO'):
            await message.channel.send('YOOOOOOOO')

        if 'beanbot' in message.content or 'Beanbot' in message.content or 'BeanBot' in message.content or 'BEANBOT' in message.content:
            await message.channel.send('GLORY TO BEANBOT')

    ##responses to @BeanBotAplha, in any server or as a DM
        if client.user.mentioned_in(message):
    #### the boon request -- add new member to beanconomy
            if 'boon' in message.content or 'Boon' in message.content or 'BOON' in message.content:
                duplicateMember = False
                for member in members:
                    if member[0] == f'{message.author}':
                        duplicateMember = True
                        print('Duplicate member rejected!!')
                if duplicateMember == False:
                    await message.channel.send(f'<@!{message.author.id}> has been granted a gift of 10 Beancoin')
                    channel = client.get_channel(798439480436326441)
                    channel.send(f'Welcome <@!{message.author.id}> to the Beanconomy')
                    welcome = [f'{message.author}','10']
                    members.append(welcome)
                    print('Beanconomy:')
                    for i in members:
                        print(i)
                    with open('BigBrainOfBeanBot.txt','w') as brain:
                        for member in members:
                            brain.writelines(member[0]+','+member[1]+'\n')
                if duplicateMember == True:
                    await message.channel.send('Nah')
            
            else:
                await message.channel.send(f'Frick off <@!{message.author.id}>')


init_logging()
init_config()
client = beanBot()
client.run(CONFIG['bot_token'])
