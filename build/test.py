import covidsim as cs

f = cs.Factory()
population = f.make_population()

f.add_cells(population, 5)

population.for_each_cell(
    lambda c: f.add_microcells(c, 2))
population.for_each_cell(
    lambda c: c.for_each_microcell(lambda m: f.add_people(m, 4)))

population.for_each_cell(
    lambda c: c.for_each_microcell(
        lambda m: m.for_each_person(
            lambda x: x.print())))
population.for_each_cell(
    lambda c: c.for_each_microcell(
        lambda m: m.print()))
population.for_each_cell(lambda c: c.print())
population.print()

