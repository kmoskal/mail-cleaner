# Mail-Cleaner
### Simple script to clean your mailbox from unwanted messages.

--- 
###### The script is based on IMAP library. Creates strings from the given keys and values from json file.
###### Then strings are used to find specific messages and then delete them.
---

##### First configure the host and credentials in *config.json*, and then change the file permissions to read only.

```bash
chmod 400 config.json
```

##### Next configure keys and values in *filter.json* file:

* **"FROM"** - e-mail address from which you don't want a message.
* **"BEFORE"** - delete messages older than X days.
* **"SUBJECT"** - deletes messages if there is a specific word/words in the subject.
* **"NOT FROM"** - address or list of addresses from you want to keep messages.


##### The keys can be combined with each other, example:
```javascript
{
    "FROM": "unwanted@email.com",
    "NOT FROM": ["this@stays.com", "andthis@stays.com", "this@stays.too.pl"],
    "SUBJECT": "Deletes emails with a given subject but NOT FROM selected contacts.",
    "BEFORE": 14
}
```

##### The types of keys can be found at [Internet Message Access Protocol document.](https://tools.ietf.org/html/rfc2060#section-6.4.4)
###### Only these four types of keys have been tested
