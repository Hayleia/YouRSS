# YouRSS

This allows someone to receive notifications about new videos on Youtube channels without using any Youtube account. It sends notifications as Discord private messages.

## How to use

Install dependencies (see imports at the beginning of check.py).
Use `crontab -e` to run check.py every 10 or 20 minutes or so. Tested with Python 3.7.
Put your Discord bot's token in .env.
Create a file named `config.json` that looks like this.
```
{
	"users": [
		0123456789123456789,
		0
	],
	"channels" : [
		["aZDGgdADadgGAGdAADfdaadf", "Some Channel"],
		["hFSsSSFHHhFZZrfdggDqQdgD", "Another Channel"],
		["", "the end"]
	]
}
```
