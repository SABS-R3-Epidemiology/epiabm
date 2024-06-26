********
Outputs
********

.. currentmodule:: pyEpiabm.output

Output provides various methods to record the outputs of any simulation or methods.

Overview:

- :class:`AbstractReporter`
- :class:`_CsvDictWriter`
- :class:`_CsvWriter`
- :class:`NewCasesWriter`
- :class:`AgeStratifiedNewCasesWriter`

.. autoclass:: AbstractReporter
    :members:
    :special-members: __init__, __call__

.. autoclass:: _CsvDictWriter
    :members:
    :special-members: __init__, __del__

.. autoclass:: _CsvWriter
    :members:
    :special-members: __init__, __del__

.. autoclass:: NewCasesWriter
    :members: write
    :special-members: __init__

.. autoclass:: AgeStratifiedNewCasesWriter
    :members: write
    :special-members: __init__
