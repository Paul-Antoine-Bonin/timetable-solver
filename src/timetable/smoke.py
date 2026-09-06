"""A five-line assignment problem, solved, to prove the solver is really there.

This module exists for one reason: `import ortools` succeeding says nothing about
whether a model can be built and solved on this machine. OR-Tools ships a compiled
solver, and the failure mode of a bad wheel is not an ImportError but a crash or a
silent `UNKNOWN` the first time `Solve` is called. So the check here builds an
actual model, adds the two constraint shapes the real timetable will be made of,
solves it, and asserts the answer is the one that can be worked out by hand.

**Why CP-SAT rather than PuLP.** The roadmap allows either. Timetabling is almost
entirely booleans and clash constraints, which is what `AddAtMostOne` and
`AddExactlyOne` express directly and what CP-SAT propagates on; the same model in
PuLP goes to CBC as a plain MILP and loses that structure. The other half of the
reason is diagnostic: when a timetable turns out infeasible, and the roadmap says
plainly that it will, CP-SAT can be asked which assumptions are in the conflict.
CBC can only say `Infeasible`.

The toy case is one group, two courses, two slots and one room. Each course needs
exactly one slot, the room holds one course at a time, so the only solutions are
the two orderings. That is the smallest case that exercises both constraint kinds
and still has a checkable answer.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

from ortools.sat.python import cp_model

COURSES = ("maths", "physics")
SLOTS = (0, 1)


@dataclass(frozen=True)
class SmokeResult:
    """What the toy solve produced."""

    status_name: str
    assignment: Dict[str, int]
    wall_time: float

    @property
    def solved(self) -> bool:
        return self.status_name in ("OPTIMAL", "FEASIBLE")


def solve_smoke(
    courses: Sequence[str] = COURSES, slots: Sequence[int] = SLOTS
) -> SmokeResult:
    """Assign each course to one slot, one course per slot, and return the result.

    Feasible only when there are at least as many slots as courses; the caller is
    expected to pass a case where that holds, and an infeasible status is reported
    rather than raised so a test can assert on it.
    """
    model = cp_model.CpModel()

    # x[course, slot] is true when that course is taught in that slot. Every model
    # in this project will be built out of booleans of this shape.
    x: Dict[Tuple[str, int], cp_model.IntVar] = {
        (course, slot): model.NewBoolVar(f"x[{course},{slot}]")
        for course in courses
        for slot in slots
    }

    # Volume: each course happens exactly once.
    for course in courses:
        model.AddExactlyOne(x[course, slot] for slot in slots)

    # Clash: the single room holds at most one course per slot.
    for slot in slots:
        model.AddAtMostOne(x[course, slot] for course in courses)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 10.0
    status = solver.Solve(model)

    assignment: Dict[str, int] = {}
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        for course in courses:
            for slot in slots:
                if solver.Value(x[course, slot]):
                    assignment[course] = slot

    return SmokeResult(
        status_name=solver.StatusName(status),
        assignment=assignment,
        wall_time=solver.WallTime(),
    )


def main(argv: Optional[Sequence[str]] = None) -> int:
    result = solve_smoke()
    print(f"status: {result.status_name}")
    for course, slot in sorted(result.assignment.items(), key=lambda kv: kv[1]):
        print(f"  slot {slot}: {course}")
    print(f"solved in {result.wall_time:.4f}s")
    return 0 if result.solved else 1


if __name__ == "__main__":
    raise SystemExit(main())
