# llm-prompt-snapshot-diff

Snapshot tests for prompts. Render each prompt template with fixed
variables, store the result, and fail when a later edit changes the text
the model would actually see. The failure shows a unified diff and the
estimated token delta, so a wording change is reviewed like any other diff.

Runs offline with the standard library only.

## Layout

```
prompts/summarize.txt          template, variables written as {{name}}
cases/summarize-short.json     {"template": "summarize.txt", "vars": {...}}
snapshots/summarize-short.txt  the approved rendered output
```

## Usage

```
python3 -m promptsnap check      # compare every case with its snapshot
python3 -m promptsnap update     # rewrite snapshots after an intended change
python3 -m unittest discover -s tests
```

`check` exits 1 on any drift, missing snapshot or render error.

## Notes

- Rendering is strict: a missing or unused variable is an error, so a case
  cannot stay green while ignoring one of its inputs.
- Substituted values are never re-scanned, so text that looks like a
  placeholder stays literal.
- Token deltas use a 4-characters-per-token estimate. Treat them as a
  size signal, not a bill.
- `make validate` runs the unit tests and the snapshot check; CI does the same.
