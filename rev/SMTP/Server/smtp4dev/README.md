# <img src='Rnwood.Smtp4dev/ClientApp/public/logo.png' alt='logo'/>
**smtp4dev - the fake SMTP email server for development and testing.**



# ***Building Instructions***

- Install dotnet 8 (so 8.10)
- CD Into project directory
- `dotnet restore`
- cd to /smtp4dev/Rnwood.Smtp4dev

**Install and update nvm**
- `curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash`

 ```export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm```

- `source ~/.bashrc  # or source ~/.bash_profile or source ~/.zshrc`
- `nvm install 18 `
- `nvm use 18`
- `nvm alias default 18`

**Update NPM**
- `npm install -g npm@latest`

**Build project (Run it maybe)**
- `cd Rnwood.Smtp4dev`
-`dotnet build`
- `dotnet run`

**Shove it to docker**
- `dotnet publish -c Release -o out`
- `docker build -f Dockerfile.linux -t magpiesmtp .`

## Getting Started
[Installation Instructions](https://github.com/rnwood/smtp4dev/wiki/Installation)

[Configuration](https://github.com/rnwood/smtp4dev/wiki/Configuration)

[Configuring your programs to send mails to smtp4dev](https://github.com/rnwood/smtp4dev/wiki/Configuring-Clients)

[API] (https://github.com/rnwood/smtp4dev/wiki/API)



## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Frnwood%2Fsmtp4dev.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Frnwood%2Fsmtp4dev?ref=badge_large)
