set -x EDITOR /usr/local/bin/vim
set -xg LC_ALL ja_JP.UTF-8
set -xg LANG ja_JP.UTF-8

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

# pyenv等のconfigがbrew doctorに引っかかってしまう問題の対応
# https://qiita.com/takuya0301/items/695f42f6904e979f0152
function brew
  set -x PATH /usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/sbin:/sbin
  command brew $argv
end


#set -g fish_user_paths "/usr/local/opt/icu4c/bin" $fish_user_paths
#set -g fish_user_paths "/usr/local/opt/icu4c/sbin" $fish_user_paths
set -x PATH /usr/local/opt/icu4c/bin $PATH
set -x PATH /usr/local/opt/icu4c/sbin $PATH

# direnv
eval (direnv hook fish)

# Since this `/usr/local/bin` has priority over the path setting by fisherman's pyenv plugin, I commented out.
# `echo{ There is also `/usr/local/bin` properly behind pyenv.
# (until that time it was defined twice before and after pyenv)
#set -x PATH /usr/local/bin $PATH
#
set -x PYTHONUSERBASE $HOME/.local
set -x PATH $PYTHONUSERBASE/bin $PATH


# Path to your custom folder (default path is $FISH/custom)
set fish_custom $HOME/.config/fish

# load secret config (API keys, etc.)
. $fish_custom/config.secret.fish

# for pipenv
set -x PIPENV_DEFAULT_PYTHON_VERSION 3
set -x PIPENV_SHELL_FANCY 1
set -x PIPENV_VENV_IN_PROJECT 1

# for poetry
set -x PATH $HOME/.poetry/bin $PATH

# Golang
set -x GOPATH $HOME/.go
set -x PATH $GOPATH/bin $PATH

set -g XDG_CONFIG_HOME "$HOME/.config"
set -g XDG_CACHE_HOME "$HOME/.cache"

# Rust
set -x PATH $HOME/.cargo/bin $PATH

# For conda
# source (conda info --root)/etc/fish/conf.d/conda.fish


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
