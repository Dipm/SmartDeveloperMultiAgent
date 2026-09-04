---
name: map-tests
description: Locate existing tests for the files in context and note which will need updates. Use when the context agent maps test coverage. Do not write or run tests.
disable-model-invocation: true
---

# Map tests

For each relevant application file, look for colocated and conventionally named
tests, for example:

- `foo.test.*` / `foo.spec.*` next to `foo.*`
- `__tests__/`, `tests/`, `test/` mirrors of the same path
- names from triage (error, handler, screen) under the test tree

For each test file you keep: path, what it asserts today, `likely need update: yes/no`.

`yes` if acceptance criteria would fail or the behavior under change is asserted.
`no` if it only imports the module or tests an untouched branch.

Note pre-existing gaps. Do not write tests, do not run the suite, do not "fix"
flaky tests. `@test` owns that.
