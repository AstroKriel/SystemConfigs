# Python: Classes and Data Structures

How to structure Python classes, enums, and dataclasses.

---

## Classes

| Rule | Detail |
|---|---|
| Private classes | leading underscore; implementation details supporting public classes; not re-exported |

```python
class _<Name>:
    ...
```

---

## Enums

| Enum type | Base classes |
|---|---|
| Used as strings | `str, Enum` |
| Pure value holder | `Enum` |

```python
class <Name>(str, Enum): ...   # used as strings
class <Name>(Enum): ...        # pure value holder
```

Enum members may hold dataclass instances as values to carry rich metadata per member:

```python
class <EnumName>(Enum):
    <MEMBER> = <DataclassType>(
        <arg>,
        <arg>,
        <arg>,
    )
```

---

## Dataclasses

| Rule | Detail |
|---|---|
| Containers | prefer `@dataclass(frozen=True)`, immutability by default |
| Derived attributes | use `@cached_property` |
| Alternative constructors | `@classmethod` methods named for the operation and source: `from_<type>` for pure type conversion, `load_from_<source>` for I/O reads |
| Resource lifecycle | use context managers (`__enter__` / `__exit__`) |
| `@property` vs `get_*` | use `@property` for attributes derived from existing state: no parameters, no side effects, cheap to compute; use `get_*` for operations that take parameters, involve I/O, or significant cost |
| Method ordering | `__post_init__`, private helpers (`_`), `@property`, `@cached_property`, instance methods, `@classmethod` |
