# Aliases
alias ll='ls -lha'
alias yz='yazi' 
alias nv='nvim'

# System Variables
EDITOR="nvim"

# Starship
export STARSHIP_CONFIG=~/.config/starship.toml
eval "$(starship init zsh)"

# Added by cua-driver-rs installer — see https://github.com/trycua/cua
export PATH="/Users/hexlo/.local/bin:$PATH"

# Unity CLI
. "/Users/hexlo/.unity/env"
