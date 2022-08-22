# WannaChat
Feeling lonely? Start swiping and find your new chat partner!

WannaChat discord bot is a tinder like discord bot. Login, create a profile and start swiping. If you match with someone, you will get the name you can add as your friend! 

<img src="https://github.com/JannesT3011/WannaChat/blob/main/logo.png" alt="LOGO"> 

![Discord Bots](https://top.gg/api/widget/servers/979065679376437308.svg) ![Discord Bots](https://top.gg/api/widget/upvotes/979065679376437308.svg)

[top.gg]( https://top.gg/bot/979065679376437308 )


### How to Start:

1. Login with wc.login
2. Update your profile with wc.profile `<category>`
3. Start swiping and find your chatpartner with wc.swipe
4. Have fun and start chatting! 🔥

### Commands
- /login: Create an account
- /logout: Delete your account
- /profile: View your profile
- /age : Set your age
- /language add <language>: Add language
- /language remove <language>: Remove language
- /gender : Set your gender
- /interests add <interest>: Add interest
- /interests remove <interest>: Remove interest
- /aboutme <aboutme_text>: Set your AboutMe text
- /bug : Report a bug
- /suggestions : Submit new feature suggestion
- /likedby: See the users who liked you
- /reset: Reset your likes and dislikes
- /reset likes: Reset your likes
- /reset dislikes: Reset your dislikes
##### Owner:
- /stats: See the users and guild
- wc.sync: Sync all slash commands

### Config
The config.py should look like this:
```python
# BOT CONFIG
TOKEN = ""
PREFIX = ""
OWNERID = ""
BLACKLIST_FILE_PATH = "data/blacklist.txt"
EMBED_COLOR = 0xBDDDF4
SUPPORT_SERVER_LINK = ""
LIMIT_LIKES = 50
# DATABASE CONFIG STUFF
CONNECTION = ""
CLUSTER = ""
DB = ""
QUEUEDB = ""
# TOP.GG
TOPGG_TOKEN = ""
```

### What data will be collected?
The bot only collect and store your UserID and your user name to link it to your profile.
Any other data, liked you age etc. will be provided by yourself.

### Privacy Policy:
The data (means: the data you provide by yourself, such as your age) will only be available for you and other users, using this bot! 
If you use the GlobalChat function, your message content (you send in the GlobalChat) will be shared on other server using the same function.


### TODOs
- [ ] valid language
- [X] bug command (submit bug to owner/support server)
- [X] suggestion/idea (submit idea to owner/support server)
- [X] Premium: See who liked you! (direct match with them!) ()
- [X] Vote benefit > limit likes (50) if not voted!
- [X] Vote log for server (give server role)
- [ ] on_timeout
- [X] slash commands
- [X] message not deleting after no more users
- [ ] top.gg images for README
- [X] On Join message with button > Click button to create WannaMeme account! (try, except)
- [X] error log
- [ ] process_error
- [ ] news > github api
- [ ] AI chat with bot
- [ ] report
- [ ] meme (link from reddit or other trustful memes sites)
- [ ] random command > returns random user who liked you!
- [ ] Business contacts
- [ ] Filter (age/gender)
- [ ] server feature (random chatpartner only on server?)
- [ ] ask for age, interests, language (...) after login
- [ ] global chat
- [ ] global polls
- [ ] global job portal
- [ ] customize profile with own emojis and other stuff (premium)
- [ ] global search for gaming partners
- [ ] PREMIUM: Send links to Chat (Filter links)
- [ ] Coins for message? Or some building Game for GlobalChat
- [ ] Show profile (age on globlachat)
- [X] GlobalChat Blacklist users
- [ ] GlobalChat Premium Anonymous mode
- [ ] Beim schreiben und matchen zufällig Tiere/emojis finden -> werden im Profil angezeigt (Sammlung!) Rarity: List of most used Emojis!
-> Collect, Trade ...
- [X] NUR NOCH SLASH COMMANDS (ADMIN COMMANDS NUR FÜR EINEN SERVER!!) BIS 1 SEp
- [ ] Alle daten in die DB packen, damit man nicht bei kleineren sachen restarten muss