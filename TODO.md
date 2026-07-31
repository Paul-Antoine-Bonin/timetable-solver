# timetable-solver: building a timetable with linear programming

## Goal
Take a real assignment problem (slots, rooms, teachers, groups) and solve it properly
with integer linear programming. Then compare the optimal solution to the timetable
actually in use.

## Data
- An anonymised real case from your school, or a synthetic set of comparable size.
- Anonymise the names before any commit.

## Steps
- [ ] Set up repo, PuLP or OR-Tools dependency
- [ ] Formalise the problem: decision variables, what an assigned slot means
- [ ] Hard constraints: no room clash, no teacher clash, no group clash, room capacity
- [ ] Volume constraints: every course must get its number of hours
- [ ] Objective function v1: minimise gaps in the students' days
- [ ] Solve, check feasibility, measure the computation time
- [ ] Objective function v2: minimise movement between buildings
- [ ] Show the tradeoff between the two objectives, the Pareto front
- [ ] Compare against the real timetable, numbers in hand
- [ ] Study robustness: what happens if a room becomes unavailable?
- [ ] Visualisation: a readable weekly grid
- [ ] README: the model, the constraints, and the measured gain

## Done when
The solver produces a feasible timetable on a realistic case, and the README puts a
number on the improvement for at least one criterion.

## Traps
- An infeasible model is the most common outcome, so plan from the start for a way to
      identify which constraint is blocking.
- The size explodes fast. Start on a subset: one cohort, one week.
