set -x EDITOR /usr/local/bin/vim
set -xg LC_ALL ja_JP.UTF-8
set -xg LANG ja_JP.UTF-8

# XDG Base Directory Specification
set -x XDG_CONFIG_HOME "$HOME/.config"
set -x XDG_CACHE_HOME "$HOME/.cache"
set -x XDG_DATA_HOME "$HOME/.local/share"

# alias
alias ls "lsd"
alias l "ls"
alias mkdirs "mkdir -p"
alias pe "pipenv"
alias pei "pipenv install"
alias per "pipenv run"
alias pes "pipenv shell"
alias twitter "open -na 'Google Chrome' --args '--app=https://mobile.twitter.com'"
alias deck "open -na 'Google Chrome' --args '--app=https://tweetdeck.twitter.com'"
alias fig "docker-compose"

set -x PATH /usr/local/opt/icu4c/bin $PATH
set -x PATH /usr/local/opt/icu4c/sbin $PATH

# direnv
eval (direnv hook fish)

set -x PYTHONUSERBASE $HOME/.local
set -x PATH $PYTHONUSERBASE/bin $PATH


# Path to your custom folder (default path is $FISH/custom)
set fish_custom $XDG_CONFIG_HOME/fish

# load secret config (API keys, etc.)
. $fish_custom/config.secret.fish

# Python
set -x PYTHONSTARTUP $XDG_CONFIG_HOME/python/startup.py

# for pipenv
set -x PIPENV_DEFAULT_PYTHON_VERSION 3
set -x PIPENV_SHELL_FANCY 1
set -x PIPENV_VENV_IN_PROJECT 1

# for poetry
set -x PATH $HOME/.poetry/bin $PATH

# ptpython
set -x PTPYTHON_CONFIG_HOME $XDG_CONFIG_HOME/ptpython/config.py

# Golang
set -x GOPATH $HOME/.go
set -x PATH $GOPATH/bin $PATH

# Rust
set -x PATH $HOME/.cargo/bin $PATH

# For fzf
set -x FZF_DEFAULT_OPTS "--height 40% --reverse --border"
set -x FZF_LEGACY_KEYBINDINGS 0

set -x PATH /usr/local/opt/curl/bin $PATH
set -x PATH /usr/local/opt/openssl@1.1/bin $PATH
set -g fish_user_paths "/usr/local/opt/gettext/bin" $fish_user_paths

# starship
starship init fish | source

set -gx VOLTA_HOME "$HOME/.volta"
set -gx PATH "$VOLTA_HOME/bin" $PATH
