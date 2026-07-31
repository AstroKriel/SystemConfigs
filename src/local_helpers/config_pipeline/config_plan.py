## { MODULE

##
## === DEPENDENCIES
##

## stdlib
from dataclasses import dataclass

##
## === CONSTANTS
##

## `PLN-1`. `render` and `post-hook` have no schema support yet
## (`config_spec.py` parses only `install` and `link`); `resolve_config`
## never emits them today, but the kind set is declared in full so a future
## schema addition does not also need a `config_plan.py` change.
STEP_ACTIONS = ("install", "render", "link", "copy", "post-hook", "teardown")

##
## === TYPES
##


@dataclass(frozen=True)
class Step:
    """
    One ordered `config_plan` step (`PLN-1`).

    Exactly one of `concept` or `pkg` is set: a bare-package `install` step
    carries `pkg` (`DEP-2`); every other step, including a concept `install`,
    is concept-scoped and carries `concept`.
    """

    action: str
    concept: str | None
    pkg: str | None


@dataclass(frozen=True)
class ConfigPlan:
    """
    The flat, ordered, host-resolved step sequence `resolve_config` produces
    (`PLN`); the third and final pipeline artefact (`ov#19`, "no third
    artefact" other than this and the config registry).

    Deterministic (`PLN-4`, `PLN-5`): identical `(filtered_config_registry,
    system_descriptor, profile)` inputs yield byte-identical `steps`.
    """

    steps: tuple[Step, ...]


## } MODULE
