# Transportation Problem

A **Linear Programming (LP)** model in **Python** for the classic **Transportation Problem**, built with the **[Pyomo](http://www.pyomo.org/)** optimization framework and solved via the **IBM ILOG CPLEX** solver. Instance data is provided alongside the script in an **Excel workbook**.

## Overview

The Transportation Problem is a fundamental network flow optimization problem in Operations Research. Goods are produced at $m$ supply centers and must be shipped to $n$ demand centers to satisfy known demand — at minimum total shipping cost.

Each supply center has a maximum capacity it cannot exceed, and each demand center must receive exactly its required quantity. Before solving, the model checks a **feasibility condition**: total supply must be at least equal to total demand, with a descriptive message printed when it is not satisfied.

## Repository Contents

| File | Description |
|---|---|
| `Transportation_Problem.py` | Python script implementing and solving the Transportation Problem via Pyomo and CPLEX |
| `Transportation_Problem_Results.txt` | Solver output: execution time, status, optimal cost, and active shipment flows |
| `Transportation_Problem.xlsx` | Excel workbook containing the problem instance data (cost matrix, supply, demand) |
| `Transportation Problem_Math Formulation.pdf` | Mathematical formulation of the problem |

## Mathematical Formulation

### Sets and Parameters

- $m$ = number of supply centers (index $i = 1, \dots, m$)
- $n$ = number of demand centers (index $j = 1, \dots, n$)
- $S_i$ = supply available at supply center $i$
- $d_j$ = demand required at demand center $j$
- $c_{ij}$ = unit shipping cost from supply center $i$ to demand center $j$

### Feasibility Condition

The problem has a feasible solution only if total supply is sufficient to cover total demand:

$$
\displaystyle \sum_{j=1}^{n} d_j \le \sum_{i=1}^{m} S_i
$$

### Variable

- $x_{ij}$ = number of units shipped from supply center $i$ to demand center $j$; $x_{ij} \ge 0$

### Objective Function

**(1)** — Minimize total shipping cost

$$
\displaystyle \min \sum_{i=1}^{m} \sum_{j=1}^{n} c_{ij} \cdot x_{ij}
$$

### Constraints

**(2)** — Supply capacity: shipments from each supply center cannot exceed its available supply

$$
\displaystyle \sum_{j=1}^{n} x_{ij} \le S_i \qquad \forall\, i = 1, \dots, m
$$

**(3)** — Demand satisfaction: each demand center must receive exactly its required quantity

$$
\displaystyle \sum_{i=1}^{m} x_{ij} = d_j \qquad \forall\, j = 1, \dots, n
$$

**(4)** — Non-negative shipments

$$
x_{ij} \ge 0 \qquad \forall\, i = 1, \dots, m,\ j = 1, \dots, n
$$

> **Note on integrality:** In this implementation, $x_{ij}$ is modeled as a **continuous** variable (the integer constraint is commented out in the code). This is intentional: the transportation problem's constraint matrix is totally unimodular, so the LP relaxation always yields an integer optimal solution when supply and demand values are integer — no explicit integrality is needed. The `within=Integers` declaration can be uncommented to enforce integrality explicitly, depending on the nature of the goods being shipped.

A copy of this formulation is also available as a standalone PDF in this repository.

## Example Instance

The script uses a hardcoded instance with **3 supply centers** and **4 demand centers**:

**Supply capacities:**

| Supply center | Capacity $S_i$ |
|:---:|---:|
| $S_1$ | 150 |
| $S_2$ | 20 |
| $S_3$ | 130 |
| **Total** | **300** |

**Demand requirements:**

| Demand center | Demand $d_j$ |
|:---:|---:|
| $D_1$ | 135 |
| $D_2$ | 75 |
| $D_3$ | 45 |
| $D_4$ | 45 |
| **Total** | **300** |

**Unit shipping cost matrix $C$:**

$$
C = \begin{pmatrix}
5 & 2 & 3 & 9 \\
7 & 1 & 12 & 4 \\
8 & 15 & 19 & 2
\end{pmatrix}
$$

This is a **balanced** instance: total supply (300) equals total demand (300), so the feasibility condition holds and all supply is fully allocated. The instance data is also available in the included Excel workbook `Transportation_Problem.xlsx`.

The **optimal total cost is 1,285**, found in **0.05 seconds**. The active shipment flows are:

| From | To | Units | Unit cost | Flow cost |
|:---:|:---:|---:|---:|---:|
| $S_1$ | $D_1$ | 50 | 5 | 250 |
| $S_1$ | $D_2$ | 55 | 2 | 110 |
| $S_1$ | $D_3$ | 45 | 3 | 135 |
| $S_2$ | $D_2$ | 20 | 1 | 20 |
| $S_3$ | $D_1$ | 85 | 8 | 680 |
| $S_3$ | $D_4$ | 45 | 2 | 90 |
| | | | **Total** | **1,285** |

Only 5 of the 12 possible arcs are active in the optimal solution. Supply center $S_2$ ships exclusively to $D_2$ (the cheapest arc available to it), while $S_1$ supplies three demand centers taking advantage of its low unit costs.

## Requirements

Install the required Python packages via pip:

```bash
pip install pyomo numpy pandas
```

**IBM ILOG CPLEX** must also be installed separately on your system. An academic license is available free of charge through the [IBM Academic Initiative](https://www.ibm.com/academic).

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/Diego-Fabbri/Transportation_Problem_Py.git
   cd Transportation_Problem_Py
   ```

2. Run the script:
   ```bash
   python Transportation_Problem.py
   ```

## Output

When executed, the script:
- Checks the feasibility condition (total supply vs total demand)
- Builds the LP model using Pyomo's `ConcreteModel` and prints the full model structure to the console
- Solves it via CPLEX and measures the execution time
- Writes the results to `Transportation_Problem_Results.txt`, including:
  - Execution time in seconds
  - Solver status and termination condition
  - Optimal total shipping cost (objective value)
  - Active shipment flows $x[i][j] > 0$ with quantity and individual cost for each route
