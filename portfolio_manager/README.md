# Corporate Capital Budgeting & Portfolio Management Engine
A modular, object-oriented Python terminal application built to evaluate corporate capital budgets and manage multi-asset investment portfolios. 

## Software Architecture & Architecture Map
The application is structured into four core decoupled operational modules:
- `holding.py`: Defines the foundational `Holding` entity class, utilizing object-oriented comparison logic and encapsulating base asset cost frameworks.
- `calculator.py`: An algorithmic financial math engine executing **Net Present Value (NPV)**, **Return on Investment (ROI)**, and **Payback Period** equations, alongside an iterative **Internal Rate of Return (IRR)** solver utilizing recursive binary search algorithms.
- `portfolio.py`: Acts as the asset collection container class utilizing object composition matrices and explicit mathematical asset weighing models.
- `main.py`: The administrative controller shell managing the interactive menu loop and wrapping user entries in strict `try/except` guard clause exception traps.

## Implemented Core Financial Formulas
- **Net Present Value (NPV):** $NPV = -I_0 + \sum_{t=1}^n \frac{CF_t}{(1+r)^t}$
- **Return on Investment (ROI):** $ROI = \frac{\text{Final Value} - \text{Initial Investment}}{\text{Initial Investment}} \times 100$
- **Payback Period:** $\text{Whole Years Elapsed} + \left( \frac{\text{Unrecovered Capital Balance}}{\text{Current Year Cash Flow}} \right)$
- **Internal Rate of Return (IRR):** Resolves the target rate $r$ where $NPV = 0$ iteratively through structural dichotomy boundaries.

## Execution Instructions
To launch the interactive terminal dashboard menu loop, execute the runtime coordinator file directly:

```bash
python main.py
```

## Key Python Features Showcased
- **Object-Oriented Programming (OOP):** Class constructors, private attributes, and composition metrics.
- **Dunder Method Implementations:** Leveraging `__len__`, `__iter__`, and `__eq__` hooks to map behaviors natively.
- **Algorithmic Optimizations:** Using a specialized high-precision recursive interval search loop for nonlinear equations.
- **Resilient Error Management:** Customized exception classes inherited from base layers to trap data errors safely.
- **Data Persistence:** Automated file serialization and deserialization via a custom JSON parser pipeline.