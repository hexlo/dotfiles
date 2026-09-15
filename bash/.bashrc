# Aliases
[ -f "/home/hexlo/dotfiles/bash/aliases.sh" ] && source "/home/hexlo/dotfiles/bash/aliases.sh"

# System Variables
export EDITOR="nvim"

# Starship
export STARSHIP_CONFIG=~/starship.toml
eval "$(starship init bash)"

# emacs
export PATH="/home/hexlo/.config/emacs/bin:$PATH"
