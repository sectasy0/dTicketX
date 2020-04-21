# dTicketX 1.0
> Discord ticketing system for you server.
> .. and much more

![Alt text](/img/discord1.png?raw=true "Screenshot1")
![Alt text](/img/discord2.png?raw=true "Screenshot2")

### Installation
```sh
$ virtualenv auth
$ cd auth && source bin/active
$ git clone https://github.com/LSDkk5/dTicketX
$ pip install -r src/REQUIREMENTS.txt
```

### Setup bot app https://discordapp.com/developers/
#### 1. Create bot app on discord developers site
![Alt text](/img/step1.png?raw=true "Create bot app")
#### 2. Copy your app token and paste to main.py
![Alt text](/img/step2.png?raw=true "Get app token")
> Put your token to run.py
#### 3. Go to the OAuth tab
![Alt text](/img/step3.png?raw=true "OAuth tab")
#### 5. Set app permissions and get join link
![Alt text](/img/step3.png?raw=true "Get join link")


### Configuration settings.json
```jsonc
{
    "warns": {
        "ban-warns-reach": true,

        "max-warns": 3,
        "ban-time": 10800
    },// That funcionality is under development yet.
    "channels": {
        "support-channel-id": 000000000000000000, // Paste channel id, where bot send initial message. 
        "support-category-id": 000000000000000000, // Paste support category id.
        "support-log-channeld-id": 000000000000000000 // Paste channel id where will be send ticket logs.
                                                    // No need set at the moment.
    },
    "support-role": "ADMIN", // Name of support role.
    "enable-channel-logger": true // if true bot send logs to support log channel.
                                    // not implemented yet
}
```

### Commands
##### ^load extension_name - loads extension
##### ^unload extension_name - unloads extension

### Todo
- [ ] Warn system
- [ ] Tempbans
- [ ] More roles support
- [ ] Channel logs
- [ ] Log ticket channels

### Contributing
- Fork this repository
- Clone this repo to your local machine
- Hack away!
- Create a new pull request

### Contact with me
- Email: lsddev@gmail.com

### Support me
[<img src="/img/paypal.png">](https://www.paypal.me/wr4ith5)
