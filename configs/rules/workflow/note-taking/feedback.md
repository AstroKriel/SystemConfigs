# Notes: Feedback

Findings raised while working in one context that feed back into your own rules, tools, or other projects; each collects in a `feedback/` folder of the `<topic>` or thread that raised it.

---

## Scope

Work on one thing often teaches something about another: a convention worth a rule, a change a library needs, a question for another project. `feedback/` holds these findings until time is set aside to act on them.

Feedback here means feedback into your own system. It is not feedback to other people.

| Finding | Goes in |
|---|---|
| You will act on it yourself, somewhere else, later | `feedback/` |
| The thread or project produces it for someone else, e.g. a proposal or a telecon plan | `notes/` |
| It is about the context itself, e.g. a pending change to the tool the note is about | that context: `tasks.md`, `log.md`, or a thread |

A thread whose purpose is to write rules keeps its drafts in its own `notes/`; they are its product, not feedback.

---

## Where it goes

`feedback/` sits in the smallest place that holds the evidence for the finding:

- a thread, when the finding came out of that thread;
- the `<topic>` itself, when it came from general work there.

Each file is named after the target:

```text
<topic>/feedback/
├── rules.md      # conventions headed for <rules>/
├── <tool>.md     # changes headed for one of your tools or libraries
└── <project>.md  # findings headed for another project
```

---

## Entries

Each entry is a `###` heading naming the finding, then a `**Raised:**` line with the date and what prompted it.

An entry in `rules.md` also carries a `**Target:**` line with the rule file it is headed for, and is written the way the rule would read: prescriptive, in short full sentences, with a generic example.

```markdown
### <Name of the convention>

**Target:** `<rules>/<path>.md`
**Raised:** <YYYY-MM-DD>, while <what prompted it>

<The convention, as it would read in the rule.>
```

---

## Acting on feedback

When time is set aside for a target, gather its entries across all notes by file name:

```bash
find <project-notes> -path '*/feedback/<target>.md'
```

An entry leaves `feedback/` once it is acted on. It is promoted to `<rules>/`, moved into the `tasks.md` of its target, or dropped. Nothing is filed away with feedback still in it: `feedback/` is empty before a thread or `<topic>` is archived. The last dated section of its log says where each entry went.
