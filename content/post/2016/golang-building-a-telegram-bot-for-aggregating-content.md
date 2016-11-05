+++
description = ""
author = ""
tags = ["Golang"]
title = "Golang: Building a Telegram bot for Aggregating Content"
date = "2016-11-05T22:36:10+06:00"

+++

I was looking for some fun excercises to learn Go. At the same time, I also started to feel the need of an 
automated program or simply put, a bot who can find contents from different sources and push them to a 
messaging service where I can read them all in one place. I briefly considered Facebook Messenger but settled
for Telegram as the messaging service of choice. Telegram has apps for both phones and macs/pcs. They also 
have an excellent set of well documented APIs. 

To begin with, I have already implemented pushing latest contents from my reddit front page to Telegram. The 
work in progress code can be found here: https://github.com/masnun/telegram-bot. 

### The Idea

The program has these major parts now: 

* SQLite Database (Used with `Gorm`)
* Telegram API
* Reddit API

The program will be run periodically via cron job. On each execution, it will run a set of `tasks` - one 
task would be to fetch reddit content, another task would parse my rss feed, some other task would track 
certain keywords on twitter - you get the idea! The main program is composed of these tasks and 
they would be run one after one (or may be on separate goroutines in the future?). For now I have only one 
task that fetches posts from my reddit front page. 

Since the app will have at best one user, SQLite should be fine for the use case. I chose `Gorm` as the ORM. 
In this blog post, I will quickly go through how these different parts work. 


### Using SQLite with Gorm

If you have worked with Go for a while, you probably already know about `Gorm` - it's a really nice ORM for Go. 
Installing `Gorm` is simply - 

```sh
go get -u github.com/jinzhu/gorm
```

Once we have Gorm installed, let's first define our first model. To keep track of which posts the bot has already 
pushed to Telegram, we will store the pushed posts in the database. For that, we will need one simple table where 
we can store the permalink of a post. 

Here's the `RedditPost` struct from `dao/entities.go`: 

```golang
package dao

import (
	"github.com/jinzhu/gorm"
)

// RedditPost - Struct for storing Reddit Posts
// Used by `gorm`
type RedditPost struct {
	gorm.Model
	PermaLink string
}
```
As you can see the `PermaLink` field would contain the permalink for each post. Now we write a `Init` function 
which will setup the connection, run any necessary (auto) migrations and return a `DB` handler so we can start 
making queries. Here's the code from `dao/gorm.go`: 

```go
package dao

import (
	"github.com/jinzhu/gorm"
	_ "github.com/jinzhu/gorm/dialects/sqlite" // for db
)

// Init - Initialize database and return a  handler
func Init() *gorm.DB {
	db, err := gorm.Open("sqlite3", "telegram.db")
	if err != nil {
		panic("failed to connect database")
	}

	db.AutoMigrate(&RedditPost{})

	return db
}

```

Here, we are using the `AutoMigrate` function to automatically apply any changes to the `RedditPost` model. On the 
first run, the table will be created if it does not exist. 

Finally, we need to write the functions which will actually make database operations. For our current task, 
we just need two functions: 

* One to check if the post exists already (pushed to telegram before)
* Store a new post 

I have these functionality defined in `dao/utils.go` - 

```
package dao

import (
	"fmt"
)

// Exists - check if an item exists in db
func Exists(PermaLink string) bool {
	db := Init()
	defer db.Close()
	var post RedditPost
	result := db.First(&post, "perma_link = ?", PermaLink)
	if result.Error != nil {
		errorMsg := result.Error.Error()

		if errorMsg == "record not found" {
			return false
		}

		fmt.Println(errorMsg)

	}

	return true

}

// Create post
func Create(PermaLink string) {
	db := Init()
	defer db.Close()
	var post = RedditPost{PermaLink: PermaLink}
	result := db.Create(&post)
	if result.Error != nil {
		errorMsg := result.Error.Error()
		fmt.Println(errorMsg)

	}
}
```

Each time, we first get the connection to the database by calling `Init` and then make `defer`red call to `Close()`
so the database connection is cleaned up when the function completes. Then we use the db connection to make queries. 

In the `Exists` function, I probably should have just used `Count` functionality instead of the complex `First` 
call and error checking. But I was learning and wanted to try something unconventional. One thing to note here is 
that the column name is `perma_link` instead of the struct field being `PermaLink`. This is Gorm convention to make 
the column snake case version of the struct field. We can however define our column names quite easily. 
For more details, please check their docs - http://jinzhu.me/gorm/models.html 

In the `Create` function we use `db.Create` to create the entry in database. That's all! 

### Reading our Reddit Frontpage

I am using `github.com/jzelinskie/geddit` to login to Reddit and grab the posts on the front page. Here's the 
code from `tasks/reddit.go`: 

```go
package tasks

import (
	"fmt"
	"os"

	"github.com/jzelinskie/geddit"
	"github.com/masnun/telegram-bot/dao"
	"github.com/masnun/telegram-bot/utils"
)

func PushReddit() {
	session, err := geddit.NewLoginSession(
		os.Getenv("REDDIT_USERNAME"),
		os.Getenv("REDDIT_PASSWORD"),
		"gedditAgent v1",
	)

	if err != nil {
		fmt.Println("Reddit Login Error: ", err)
		return
	}

	subOpts := geddit.ListingOptions{
		Limit: 15,
	}

	submissions, _ := session.Frontpage(geddit.DefaultPopularity, subOpts)

	for _, s := range submissions {
		if exists := dao.Exists(s.Permalink); !exists {
			fmt.Printf("Title: %s\nAuthor: %s\n\n", s.Title, s.Permalink)
			dao.Create(s.Permalink)
			utils.SendTelegramMessage(fmt.Sprintf("%s : https://www.reddit.com/%s", s.Title, s.Permalink))
		} else {
			fmt.Println("Exists: ", s.Permalink)
		}

	}

}
```

Here we first login to Reddit. The credentials are stored using environment variables. I use a file named 
`configure.sh` to `export` the variables. You can copy the existing 
<a href="https://github.com/masnun/telegram-bot/blob/master/configure.sh.sample">`configure.sh.sample`</a>
file and store it as `configure.sh`. Fill up the credentials and then do this: 

```sh
. ./configure.sh
```

This should set the environment variables. Please make sure to complete this process before you run the program. 

After connecting to reddit, we fetch 15 posts, `range` through them and if a new post is found, we post the title 
and url to Telegram. 

### Posting to Telegram

First create a bot by contacting the infamous `BotFather` on Telegram. Once you have the Token, we'll need one 
more thing - your chat ID so the bot can directly send you the message. 

First, `go get` the project we shall use to connect to Telegram: 

```sh
go get github.com/go-telegram-bot-api/telegram-bot-api
```

Then go ahead and run the sample codes available on: 
https://github.com/go-telegram-bot-api/telegram-bot-api and you can get the chat id from `update.Message.Chat.ID`.
After extracting the chat ID, store it in the `configure.sh` file. 

Now, we write a very simple function to post to our user. Here's the code from `utils/telegram.go`:

```go

package utils

import (
	"os"
	"strconv"

	"fmt"

	"gopkg.in/telegram-bot-api.v4"
)

func SendTelegramMessage(message string) {

	bot, err := tgbotapi.NewBotAPI(os.Getenv("TELEGRAM_KEY"))
	if err != nil {
		fmt.Println(err.Error())
	}

	if bot.Self.UserName == "" {
		fmt.Println("Error connecting to Telegram!")
		return
	}

	chatID, _ := strconv.ParseInt(os.Getenv("TELEGRAM_OWNER_CHATID"), 10, 64)
	msg := tgbotapi.NewMessage(chatID, message)
	bot.Send(msg)

}
```

We connect to telegram using the token we received from BotFather. Then to make sure that the auth was successful, 
we check the username of the bot. Then we construct a new message using the chat id and the message we get as 
argument. We send it. The code is pretty simple and straightforward. 

### Building and Running

First make sure you have the correct details in `configure.sh` file and you have the environment variables set. If 
not, set them: 

```sh
. ./configure.sh
``` 

Now we build and run: 

```sh

go build -o bot
./bot
```

If everything goes alright, you should see the latest reddit front page submissions are posted to your telegram :)


##### Slow Build? 

If you're using vendoring like me and you notice the build is taking slow, it's probably because of the sqlite 
driver. These should fix that: 

```sh
cd ./vendor/github.com/mattn/go-sqlite3/
go install
```


### What's next? 

I am yet to integrate other sources. Hacker News, RSS feeds, tweets and other stuff would be nice to add. 
Later it would be a good idea to implement some sort of intelligent filtering / sorting of the contents 
based on my interests/reading habits. 

I really hope to learn some Golang by building the stuff. If you notice some bad practices or scopes of 
improvement, please feel free to suggest those in the comment section. 