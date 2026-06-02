##
## === FREQUENTLY VISITED DIRECTORIES
##

create_alias_if_present --var DDWN  --alias ddwn  --dir "$DHOME/Downloads"

create_alias_if_present --var DREPOS --alias drepos --dir "$DHOME/repos"

create_alias_if_present --var DRES   --alias dres   --dir "$DREPOS/research"
create_alias_if_present --var DQUOKKA --alias dquokka --dir "$DRES/quokka"
create_alias_if_present --var DPENCIL --alias dpencil --dir "$DRES/pencil-code"
create_alias_if_present --var DASGARD --alias dasgard --dir "$DRES/Asgard"
create_alias_if_present --var DNRES   --alias dnres   --dir "$DRES/ResearchNotes"

create_alias_if_present --var DSYS   --alias dsys   --dir "$DREPOS/system"
create_alias_if_present --var DCONFIGS --alias dconfigs --dir "$DSYS/SystemConfigs"
create_alias_if_present --var DNSYS    --alias dnsys    --dir "$DSYS/SystemNotes"

create_alias_if_present --var DTEACH --alias dteach --dir "$DREPOS/teaching"
create_alias_if_present --var DBITES --alias dbites --dir "$DTEACH/BiteSizePython"

## .
