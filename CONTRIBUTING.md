# Contributing to epiabm

Thank you for taking to time to contribute to this project!

The following is a set of guidelines for contributing to epiabm, which is hosted on [GitHub](https://github.com/SABS-R3-Epidemiology/epiabm). These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## About epiabm

Epiabm implements an agent-based [SEIR model](https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology) with added compartments and spatial complexity. It immitates the Imperial [CovidSim](https://github.com/mrc-ide/covid-sim) model, but aims to simplify and clarify the model by using more user friendly software practices. It also provides various sub-models (with elements of the CovidSim model removed) for research and pedagogical investigation into the effect of different aspects of the model.

Its therefore important to us that all new features are grounded in epidemiological research, and based on methods in CovidSim. Any deviations from CovidSim, and further explanation of our model (and the parameters used) can be found in the [wiki](https://github.com/SABS-R3-Epidemiology/epiabm/wiki).

We have two backends for simulation - `pyEpiabm` and `cEpiabm`. The former is written in python, and intended as a user friendly intropduction to the software and pedagogical tool, with complete functionality but limiting performance on larger (~1 million individuals) simulations. `cEpiabm` therefore provides a high performance alternative written in C++, to handle larger and more complex simulations, whle using the same framework as both `pEpiabm` and `CovidSim`.

### Useful Resources

* [Our Wiki](https://github.com/SABS-R3-Epidemiology/epiabm/wiki) - Contains info about our model, and comparisons to CovidSim.
* [pyEpiabm Docs](https://epiabm.readthedocs.io/en/latest/) - Complete documentation for the python backend.

## Docs

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

## Testing

Tests for `pyEpiabm` use the `unittest` framework, while those in `cEpiabm` use `Catch2`. Testing is important to us, and we aim for 100% coverage in all PRs, measured using 
[codecov](https://app.codecov.io/gh/SABS-R3-Epidemiology/epiabm).

All python tests are ran from the `pyEpiabm/run_tests` directory, which also contains comprehensive documentation tests, to ensure all new modules are also included in the documentation. Further information on how to run those tests is availiable in that file, while the github workflows describe how to run the C++ tests.

We currently support python 3.6 onwards, and C++ 20.04, so ask that any contributions are also compatible with these versions.

## Submitting changes

Please send a [GitHub Pull Request to epiabm](https://github.com/SABS-R3-Epidemiology/epiabm/pull/new/master) with a clear list of what you've done (read more about [pull requests](http://help.github.com/pull-requests/)). Please follow our coding conventions (below) and make sure all of your commits are atomic (one feature per commit).

Always write a clear log message for your commits, and its helpful to quote issue numbers in the commit messages as well if relevant, eg:

```console
git commit -m "Change installation directory (#94)"
```

## Coding conventions

We have some general conventions in our `.editorconfig` [file](https://github.com/SABS-R3-Epidemiology/epiabm/blob/main/.editorconfig), and closely follow [PEP8](https://peps.python.org/pep-0008/) conventions in the python code. If you start reading our code and you'll get the hang of it, but here are a few pointers:

  * We indent using four spaces
  * We have an empty newline at the end of files
  * We have 79 characters per line, and avoid backslashes as far as possible when trying to achieve this.
  * We put spaces after list items (`[1, 2, 3]`, not `[1,2,3]`) and around operators (`x += 1`, not `x+=1`).
  * This is open source software. Consider the people who will read your code, and make it look nice for them.

We use [flake8](https://flake8.pycqa.org/en/latest/) style guide enforcement, so recommend using this to lint your code.

Thanks,
The epiabm team
