##
## === SSH AGENT
##

_load_ssh_keys_if_present() {
    local keys=()
    for key in "$@"; do
        [[ -f ~/.ssh/$key ]] && keys+=("$key")
    done
    (( ${#keys[@]} )) && eval "$(keychain --eval --quiet "${keys[@]}")"
}

if command -v keychain &>/dev/null; then
    _load_ssh_keys_if_present \
        id_ed25519_github \
        id_ed25519_aifa \
        id_ed25519_marvin
fi

## .
