# Aliases
[ -f "$HOME/dotfiles/bash/aliases.sh" ] && source "$HOME/dotfiles/bash/aliases.sh"

# System Variables
export EDITOR="nvim"

# Starship
export STARSHIP_CONFIG=~/.config/starship.toml
eval "$(starship init bash)"

# emacs
export PATH="$HOME/.config/emacs/bin:$PATH"

# rust binaries
export PATH="$HOME/.cargo/bin:$PATH"
