# timetable-solver

Building a timetable with linear programming.

Slots, rooms, teachers, groups: an assignment problem that every school solves by hand
and that integer programming solves properly. This repo builds the model, then compares
the optimal timetable to the one actually in use.

No timetable yet. What exists is the environment and a solved toy case that proves the
solver runs on this machine.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

Built against OR-Tools 9.15.6755, Python 3.13.5.

## Check the solver actually solves

```bash
python -m timetable.smoke
```

```
status: OPTIMAL
  slot 0: physics
  slot 1: maths
solved in 0.0070s
```

One group, two courses, two slots, one room. Small enough that the answer is known in
advance, large enough to exercise both constraint shapes the real model is made of:
each course happens exactly once, and the room holds at most one course per slot.

## Why CP-SAT and not PuLP

The roadmap allowed either. Timetabling is booleans and clash constraints almost
end to end, and `AddAtMostOne` / `AddExactlyOne` are exactly that: CP-SAT propagates on
the structure, while the same model handed to CBC through PuLP is a plain MILP with the
structure flattened out of it.

The second reason matters more. An infeasible model is the expected first outcome here,
not an accident, so the question "which constraint is blocking?" has to be answerable.
CP-SAT can be asked, through assumption literals and the conflict it returns. CBC
answers `Infeasible` and stops.

A dependency that imports is not a dependency that works: OR-Tools ships a compiled
solver, and a bad wheel fails on the first `Solve`, not on the import. Hence a smoke
case that builds a model and checks the answer rather than a bare `import ortools`.

## Run the tests

```bash
pytest
```

4 tests: the toy case solves to `OPTIMAL` with each course in exactly one slot and no
two courses in the same room-slot, and three courses into two slots comes back as
`INFEASIBLE` as a status rather than an exception.

Roadmap and progress: [TODO.md](TODO.md)
