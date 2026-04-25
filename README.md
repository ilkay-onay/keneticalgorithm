# KeneticAlgorithm

## Overview

KeneticAlgorithm is an open-source project developed using Python and the PyQt6 framework, designed to simulate and explore the principles of genetic algorithms. This application provides a user-friendly interface for configuring and running genetic algorithm simulations, visualizing the generation of new populations, and tracking the optimization process. It allows users to define the parameters of the genetic algorithm, including equation inputs, population size, number of generations, and mating pool size. The core functionality revolves around implementing genetic operators such as selection, crossover, and mutation to evolve a population towards an optimal solution for a given set of input equations.

## Features

*   **Parameter Configuration:** Intuitive interface for setting up genetic algorithm parameters, including:
    *   Equation inputs (up to 6)
    *   Number of weights
    *   Population size (Solutions Per Population)
    *   Range for initial population values (Min Number, Max Number)
    *   Number of generations
    *   Number of parents for mating
*   **Population Generation:** Generates an initial population based on user-defined parameters.
*   **Genetic Operators:** Implements core genetic algorithm operations:
    *   **Fitness Calculation:** Evaluates the fitness of each individual in the population based on the provided equation inputs.
    *   **Parent Selection:** Selects the fittest individuals from the population to be parents for the next generation.
    *   **Crossover:** Combines genetic material from parent individuals to create offspring.
    *   **Mutation:** Introduces random variations into the offspring to maintain diversity and explore new solution spaces.
*   **Simulation Visualization:**
    *   Displays the newly generated population in a list view.
    *   Tracks the progress of the calculation with a progress bar.
    *   Presents the results of each generation in a table, showing the best result, its fitness, and the corresponding solution.
*   **Preset Management:** Allows users to save and load algorithm configurations for reproducibility.
*   **Randomization Options:** Provides functionality to randomize equation inputs within a specified range and precision.
*   **User Interface:** Built with PyQt6, offering a modern and responsive graphical user interface.
*   **Licensing:** Distributed under the GNU General Public License v3.0, ensuring freedom to use, modify, and distribute the software.

## Project Structure

```
.
├── LICENSE
├── LICENSE.txt
├── defaultval.pkl
├── genaldef.py
├── generatepop.py
├── generatepop.ui
└── main.py
```

*   `LICENSE` / `LICENSE.txt`: Contains the GNU General Public License v3.0 text.
*   `defaultval.pkl`: A pickled file likely containing default parameter values for the genetic algorithm.
*   `genaldef.py`: Implements the core genetic algorithm functions (fitness calculation, selection, crossover, mutation).
*   `generatepop.py`: Contains the UI definition for the main application window, likely generated from the `.ui` file.
*   `generatepop.ui`: The Qt Designer UI file defining the graphical interface of the application.
*   `main.py`: The main application script that initializes the PyQt application, sets up the UI, connects signals and slots, and runs the genetic algorithm simulation.

## Getting Started

To run the KeneticAlgorithm application, you will need Python and the PyQt6 library installed.

1.  **Clone the repository** (if applicable) or download the project files.
2.  **Install PyQt6:**
    ```bash
    pip install PyQt6
    ```
3.  **Install NumPy:**
    ```bash
    pip install numpy
    ```
4.  **Run the application:**
    ```bash
    python main.py
    ```

The application will launch, presenting you with the configuration interface to set up your genetic algorithm parameters.

## License

This project is licensed under the **GNU General Public License v3.0**.

You are free to:

*   **Share** — copy and redistribute the material in any medium or format.
*   **Adapt** — remix, transform, and build upon the material for any purpose, even commercially.

The licensor cannot revoke these freedoms as long as you follow the license terms.

Under the following terms:

*   **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
*   **ShareAlike** — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.
*   **No additional restrictions** — You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.

For more details, please refer to the `LICENSE` or `LICENSE.txt` file in the repository.
