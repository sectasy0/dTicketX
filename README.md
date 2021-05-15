# dTicketX 1.1
> Discord support tickets system for you server.
> .. and much more

![Alt text](/img/discord1.png?raw=true "Screenshot1")
![Alt text](/img/discord2.png?raw=true "Screenshot2")

### Installation
```sh
$ virtualenv ticketx
$ cd ticketx && source bin/active
$ git clone https://github.com/sectasy0/dTicketX
$ pip install -r src/REQUIREMENTS.txt
```

### Setup bot app https://discordapp.com/developers/
#### 1. Create a bot app on discord developers site
![Alt text](/img/step1.png?raw=true "Create bot app")
#### 2. Copy your app token and paste to main.py
![Alt text](/img/step2.png?raw=true "Get app token")
> Put your token to run.py
#### 3. Go to the OAuth tab
![Alt text](/img/step3.png?raw=true "OAuth tab")
#### 5. Set app permissions and get join link
![Alt text](/img/step4.png?raw=true "Get join link")


### Configuration settings.json
```jsonc
{
    "warns": {
        "ban-warns-reach": true,
        "max-warns": 3,
        "ban-time": 10800
    },
    "channels": {
        "support-channel-id": 000000000000000000, // Paste channel id, where the bot sends an initial message. 
        "support-category-id": 000000000000000000, // Paste support category id.
        "support-log-channeld-id": 000000000000000000 // Paste channel id where the bot will send ticket logs.
    },
    "support-role": "ADMIN", // Name of the support role.
    "enable-channel-logger": true // if true bot send logs to support the log channel.
}
```

### Commands
##### ^load extension_name - loads extension
##### ^unload extension_name - unloads extension
##### ^warn @user <reson: optionally> - warn user

### Todo
- [X] Warn system
- [X] Tempbans
- [ ] More roles support
- [X] Channel logs
- [X] Log messages from ticket channel

### Contributing
- Fork this repository
- Clone this repository to your local machine
- Hack away!
- Create a new pull request

# Changelog
## [1.0.0] - 22/04/2020
- Complete main bot functionalities.
## [1.1.0] - 26/04/2020
- Add saving logs added to the channel.
- Add saving logs added from ticket channels to file in logs.
## [1.2.0] - 19/05/2020
- Add tempbans.
- Add warn system.
- fix bugs.

### Contact with me
- Email: lxstsoftware@gmail.com
