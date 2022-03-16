# Contributing to epiabm

Thank you for taking to time to contribute to this project!

The following is a set of guidelines for contributing to epiabm, which is hosted on [GitHub](https://github.com/SABS-R3-Epidemiology/epiabm). These are mostly guidelines, not rules, so do use your best judgement.
## About epiabm

Epiabm implements an agent-based [SEIR model](https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology) with added compartments and spatial complexity. It imitates the Imperial [CovidSim](https://github.com/mrc-ide/covid-sim) model, but aims to simplify and clarify the model by using more user friendly software practices. It also provides various sub-models (with elements of the CovidSim model removed) for research and pedagogical investigation into the effect of different aspects of the model.

It's therefore important to us that all new features are grounded in epidemiological research, and based on methods in CovidSim. Any deviations from CovidSim, and further explanation of our model (and the parameters used) can be found in the [wiki](https://github.com/SABS-R3-Epidemiology/epiabm/wiki).

We have two backends for simulation - `pyEpiabm` and `cEpiabm`. The former is written in python, and intended as a user friendly intropduction to the software and pedagogical tool, with complete functionality but limiting performance on larger (~1 million individuals) simulations. `cEpiabm` therefore provides a high performance alternative written in C++, to handle larger and more complex simulations, while using the same framework as both `pyEpiabm` and `CovidSim`.

### Useful Resources

* [Our Wiki](https://github.com/SABS-R3-Epidemiology/epiabm/wiki) - Contains info about our model, and comparisons to CovidSim.
* [pyEpiabm Docs](https://epiabm.readthedocs.io/en/latest/) - Complete documentation for the python backend.

## Workflow

### Before you start
1. Create an [issue](https://guides.github.com/features/issues/) where new proposals can be discusssed before any coding is done.
2. Create a [branch](https://help.github.com/articles/creating-and-deleting-branches-within-your-repository/) of this repo (ideally on your own [fork](https://help.github.com/articles/fork-a-repo/)), where all changes will be made
3. Download the source code onto your local system, by [cloning](https://help.github.com/articles/cloning-a-repository/) the repository (or your fork of the repository).

### Installation

To install pyEpiabm with all developer options, use:

```
$ git clone https://github.com/SABS-R3-Epidemiology/epiabm.git
$ cd epiabm/pyEpiabm
$ pip install -e .[dev,docs]
```

This will

* Install all the dependencies for epiabm, including the ones for documentation (docs) and development (dev).
* Tell Python to use your local epiabm files when you use `import epiabm` anywhere on your system.

You may also want to create a virtual environment first, using [virtualenv](https://docs.python.org/3/tutorial/venv.html) or [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html).
The installation of cEpiabm is more involved, but documented in our [README](https://github.com/SABS-R3-Epidemiology/epiabm#installation-of-cepiabm).

### Writing your code

4. Make sure to follow our [coding style guidelines](#coding-style-guidelines).
5. Commit your changes to your branch with useful, descriptive commit messages: these are publically visible and should still make sense a few months ahead in time. If relevant, quote issue numbers in the commit messages as well, e.g.:

```console
git commit -m "Change installation directory (#94)"
```

### Merging your changes

6. [Test your code!](#testing)
7. Make sure any new methods or classes you added are documented, and this builds locally, please read the [documentation](#documentation) section for more info.
8. When you feel your code is finished, run syle, docs and unit tests and then create a [pull request](https://help.github.com/articles/about-pull-requests/) (PR) on [epiabm GitHub page](https://github.com/SABS-R3-Epidemiology/epiabm/pulls).
9. Once a PR has been created, it will be reviewed by any member of the community. Changes might be suggested which you can make by simply adding new commits to the branch. When everything's finished, someone with the right GitHub permissions will merge your changes into epiabm master repository.

## Documentation

All our functions are fully documented - there are many examples in the code but here is a template for both python and C++:

```python
def person_inf(infector):
    """Calculate the time-independant infectiousness of a person.

    Parameters
    ----------
    infector : Person
        Infector

    Returns
    -------
    float
        Infectiousness parameter of person

    """
```

```cpp
/**
 * @brief Construct a new Household object
 * 
 * @param mcellPos Index of the household within the host cell
 */
Household(size_t mcellPos);
```

pyEpiabm docs can be built locally from `pyEpiabm/docs` with: `$ make html`

## Testing

Tests for `pyEpiabm` use the `unittest` framework, while those in `cEpiabm` use `Catch2`. Testing is important to us, and we aim for 100% coverage in all PRs, measured using 
[codecov](https://app.codecov.io/gh/SABS-R3-Epidemiology/epiabm).

All python tests are ran from the `pyEpiabm/run_tests` directory, which also contains comprehensive documentation tests, to ensure all new modules are also included in the documentation. Further information on how to run those tests is availiable in that file, while the github workflows describe how to run the C++ tests.

We currently support python 3.6 onwards, and C++ 20.04, so ask that any contributions are also compatible with these versions.

## Coding style Guidelines

We have some general conventions in our `.editorconfig` [file](https://github.com/SABS-R3-Epidemiology/epiabm/blob/main/.editorconfig), and closely follow [PEP8](https://peps.python.org/pep-0008/) conventions in the python code. If you start reading our code you'll get the hang of it, but here are a few pointers:

  * We indent using four spaces
  * We have an empty newline at the end of files
  * We have 79 characters per line, and avoid backslashes as far as possible when trying to achieve this.
  * We put spaces after list items (`[1, 2, 3]`, not `[1,2,3]`) and around operators (`x += 1`, not `x+=1`).
  * This is open source software. Consider the people who will read your code, and make it look nice for them.

We use [flake8](https://flake8.pycqa.org/en/latest/) style guide enforcement, so recommend using this to lint your code.

## Profiling

We currently have no speed/run time requirements in our tests, however we do ask that you bear run-time in mind when adding new functionality (and state in your PR if your changes increase the runtime of any example workflows by more than 20%). We recommend the use of [kernprof](https://github.com/pyutils/line_profiler) for profiling. This requires the `kernprof.py` file stored in the top-level directory, and the package `line-profiler`, which is pip installable. Decorate all functions you wish to profile with the following decorator:

```python
@profile
def slow_function(a, b, c):
    ...
```

Note that this decorator should be applied directly to the relevant function - this is particularly relevant where the `@log_exceptions()` decorator is also used, to prevent the output file just showing the runtime of each line in the decorator.

Then, to run profiling on the basic `simulation_flow.py` example:

```console
python3 kernprof.py -l python_examples/simulation_flow.py
```

This will create an output file in the current working directory with the same name as the file you have profiled, but an added `.lprof` extension. To view this, use:

```console
python3 -m line_profiler simulation_flow.py.lprof 
```

In this way you can identify bottlenecks in performance, or compare the time spent running your functions to the overall simulation time. Note there is a small performance cost in profiling (and the `@profile` decorator will throw errors for users who don't have this module installed), so all references to profiling in the code should be removed before submission.

Thanks,  
The [epiabm](https://github.com/SABS-R3-Epidemiology/epiabm) team
