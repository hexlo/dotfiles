# Aliases
[ -f "$(dirname "${BASH_SOURCE[0]}")/aliases.sh" ] && source "$(dirname "${BASH_SOURCE[0]}")/aliases.sh"

# System Variables
export EDITOR="nvim"

# Starship
eval "$(starship init bash)"

# emacs
export PATH="/home/hexlo/.config/emacs/bin:$PATH"
