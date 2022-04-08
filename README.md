# Project Title

CloudFlare commandline cli (python wrapper).

## Description

This project objective is to provide a command like interface to manage cloudflare dns records.
This can eventually expand to manage other areas of CloudFlare by interacting seamlessly with their v4 API

## Getting Started

clone the repository
```
git clone repository_url
```
Create python virtual environment folder
```
python -m venv venv
```
Windows venv activate environment
```
venv\Scripts\activate.bat
```
Linux and MacOS venv activate environment
```
$ source venv\Scripts\activate.bat
```
Install dependencies
pip install -r requirements.txt

### Dependencies

Python 3
Cloudflare

### Installing

Create a Cloudflare user Token and add it to .cloudflare.cfg file in project folder
(See below instructions on configuration file structure)

### Executing program

### Providing Cloudflare Username and API Key

They are retrieved from either the users exported shell environment variables or the .cloudflare.cfg or ~/.cloudflare.cfg or ~/.cloudflare/cloudflare.cfg files, in that order.

If you're using an API Token, any cloudflare.cfg file must either not contain an email attribute or be a zero length string and the CLOUDFLARE_EMAIL environment variable must be unset or be a zero length string, otherwise the token will be treated as a key and will throw an error.

There is one call that presently doesn't need any email or token certification (the /ips call); hence you can test without any values saved away.

### Using configuration file to store email and keys

The default profile name is ```Cloudflare``` for obvious reasons.

*.cloudflare.cfg*
```
[Cloudflare]
email = user@example.com # Do not set if using an API Token
token = 00000000000000000000000000000000
```

More than one profile can be stored within that file. Here's an example for a Production and Staging setup (in this example Production has an API Token and Staging uses email/token).

```
[Production]
token = 00000000000000000000000000000000
[Staging]
email = home@example.com
token = 00000000000000000000000000000000
```

### Using shell environment variables

* CLOUDFLARE_EMAIL
* CLOUDFLARE_API_KEY
* CLOUDFLARE_API_CERTKEY

Example

```
$ export CLOUDFLARE_EMAIL='user@example.com' # Don't set if using an API Token
$ export CLOUDFLARE_API_KEY='00000000000000000000000000000000'
$ export CLOUDFLARE_API_CERTKEY='v1.0-...'
```
---

**Info**

Please keep in mind that shell environment variables override values set within a configuration file.

---

## Help

Get help.
```
cloudflare.py -h
```
This app has subcommands you can use -h after to get help on subcommands
Update command help
```
cloudflare.py u -h
```
Update dns subcommand help
```
cloudflare.py u dns -h
```

## Command Execution Examples

* Update CNAME DNS record to change Content
```
cloudflare.py u dns test.com CNAME recordname.test.com content.url.com CNAME recordname.test.com newcontent.url.com
```

## Authors

## Version History

* 0.1
    * Initial Release

## License


## Acknowledgments
