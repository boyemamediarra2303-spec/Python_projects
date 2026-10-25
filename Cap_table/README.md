# 💸 Advanced Cap Table & Equity Dilution Simulator

An enterprise-grade financial simulation platform built in Python using advanced **Object-Oriented Programming (OOP)** architectures. This application models venture capital funding rounds, computes equity dilution metrics across multi-tiered investment cycles, and executes structured acquisition liquidation simulations via a polymorphic payout waterfall engine.

---

## 🏛️ Core Architectural Pillars (OOP)

This project was built to comprehensively exercise the five core pillars of production-level object design:

| OOP Pillar | Technical Implementation |
| :--- | :--- |
| **1. Abstraction** | Utilizes Python's native `abc` module to enforce a strict contract via `ShareClass`. The base class cannot be instantiated directly, forcing explicit layout definitions on child structures. |
| **2. Inheritance** | Derives concrete specialized components (`CommonShare` and `PreferredShare`) from the abstract blueprint, sharing foundational identity while branching behavior. |
| **3. Polymorphism** | Resolves core operations (`describe()` and `liquidation_multiple()`) inline on mixed item matrices without utilizing dirty type-checking loops (`isinstance`), allowing the system to scale fluidly. |
| **4. Encapsulation** | Enforces variable isolation boundaries by protecting the core asset data state (`_shares`). Direct manipulation is intercepted by a validating `@property` setter threshold, immediately halting dirty input data. |
| **5. Name Mangling** | Shields internal tracking properties (`__investor_id`) by leveraging double-underscore prefixing to cause runtime compiler adjustments, strictly exposing data via verified read-only portals. |

---

## 🧬 Project Blueprint & File Map

```text
cap_table/
├── shares.py       # Defines abstract templates and polymorphic share behaviors
├── shareholder.py  # Controls investor identities, properties, and sorting rules
├── captables.py     # The core database engine managing state modifications
├── main.py         # The interactive terminal control panel interface shell
└── data.json       # The database layer tracking states across system cycles
```

### 🧠 Advanced Fintech Capabilities Implemented
1. **The Dilution Engine Matrix:** Simulates structured equity financing rounds. It captures historical snapshot parameters, inserts new capital allocations, expands the outstanding share pool baseline, and outputs a tracking delta summary (`before` and `after` metrics).
2. **Polymorphic Exit Waterfall Simulation:** Models a real-world company acquisition liquidity event. Preferred share investment tiers are satisfied up to their specified `liquidation_multiple` thresholds *before* any remaining residual funds cascade down pro-rata into the common equity layer.
3. **Data Serialization Loop:** Circumvents traditional JSON serialization barriers by mapping custom classes down to primitive dictionary keys, enabling complete session save and recovery round-trips.

---

## ⚡ Quick Start & Run Guide

### Prerequisites
* Python 3.10 or higher installed on your computer.

### Execution
1. Open your terminal or console window.
2. Navigate directly into the root folder containing the application:
   ```bash
   cd path/to/your/folder/Cap_table
   ```
3. Boot up the interactive control station:
   ```bash
   python main.py
   ```

### Operational Workflows Available:
* **Option 1:** Populate your founding capital allocation records.
* **Option 2:** Simulate venture backing injections (supports Preferred tiers with custom preferences).
* **Option 3:** Display ownership data sorted dynamically from largest to smallest slice via `__lt__`.
* **Option 4:** Analyze precisely how your equity was compressed during the last transaction cycle.
* **Option 5:** Calculate acquisition liquidation distributions.
* **Option 6:** Commit your current workspace data safely to storage and exit cleanly.

---

## 🛠️ Automated Testing Matrix

This platform features an independent automated verification layer. Before checking in changes or pushing modifications up to production branches, run the assert engine to verify structural compliance across custom exception thresholds, property boundaries, and sorting mechanics:

```bash
python captables.py
```
*(If the engine prints a series of `✅ Shield Checked` success validations without stack trace crashes, your application state matches operational guidelines!)*
