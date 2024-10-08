
#include "dataclasses/cell.hpp"

#include "../catch/catch.hpp"

#include <random>

using namespace epiabm;

inline CellPtr makeSubject(size_t n_microcells, size_t n_people)
{
    CellPtr subject = std::make_shared<Cell>(0);
    REQUIRE(subject->index() == 0);
    for (size_t i = 0; i < n_microcells; i++)
    {
        subject->microcells().push_back(Microcell(i));
    }

    for (size_t i = 0; i < n_people * n_microcells; i++)
    {
        subject->people().push_back(Person(i%10, i, i / 10));
        subject->microcells()[i % 10].people().push_back(i);
    }

    REQUIRE(subject->microcells().size() == n_microcells);
    for (size_t i = 0; i < n_microcells; i++)
        REQUIRE(subject->microcells()[i].people().size() == n_people);
    REQUIRE(subject->people().size() == n_microcells * n_people);
    return subject;
}

TEST_CASE("dataclasses/cell: test initialize cell", "[Cell]")
{
    Cell subject = Cell(0);
    REQUIRE(subject.microcells().empty());
    REQUIRE(subject.people().empty());
}

TEST_CASE("dataclasses/cell: test add microcells", "[Cell]")
{
    Cell subject = Cell(0);
    REQUIRE(subject.microcells().empty());
    REQUIRE(subject.people().empty());

    for (size_t i = 0; i < 100; i++)
    {
        subject.microcells().push_back(Microcell(i));
    }
    REQUIRE(subject.microcells().size() == 100);

    for (size_t i = 0; i < 100; i++)
    {
        REQUIRE(subject.microcells()[i].cellPos() == i);
    }
}

TEST_CASE("dataclasses/cell: test getMicrocell", "[Cell]")
{
    Cell subject = Cell(0);
    REQUIRE(subject.microcells().empty());
    REQUIRE(subject.people().empty());

    for (size_t i = 0; i < 100; i++)
    {
        subject.microcells().push_back(Microcell(i));
    }
    REQUIRE(subject.microcells().size() == 100);

    for (size_t i = 0; i < 100; i++)
    {
        REQUIRE(subject.getMicrocell(i).cellPos() == i);
    }
}

TEST_CASE("dataclasses/cell: test add people", "[Cell]")
{
    Cell subject = Cell(0);
    REQUIRE(subject.microcells().empty());
    REQUIRE(subject.people().empty());

    for (size_t i = 0; i < 1000; i++)
    {
        subject.people().push_back(Person(0, i, 0));
    }
    REQUIRE(subject.people().size() == 1000);

    for (size_t i = 0; i < 1000; i++)
    {
        REQUIRE(subject.people()[i].cellPos() == i);
    }
}

TEST_CASE("dataclasses/cell: test getPerson", "[Cell]")
{
    Cell subject = Cell(0);
    REQUIRE(subject.microcells().empty());
    REQUIRE(subject.people().empty());

    for (size_t i = 0; i < 1000; i++)
    {
        subject.people().push_back(Person(0, i, 0));
    }
    REQUIRE(subject.people().size() == 1000);

    for (size_t i = 0; i < 1000; i++)
    {
        REQUIRE(subject.getPerson(i).cellPos() == i);
    }
}

TEST_CASE("dataclasses/cell: test add people microcells", "[Cell]")
{
    CellPtr subject = makeSubject(10, 100);

    for (size_t i = 0; i < 10; i++)
    {
        for (size_t j = 0; j < subject->microcells()[i].people().size(); j++)
        {
            REQUIRE(subject->microcells()[i].getPerson(*subject, j).microcellPos() == j);
        }
    }

    for (size_t i = 0; i < 1000; i++)
    {
        REQUIRE(subject->people()[i].cellPos() == i);
        REQUIRE(subject->people()[i].microcellPos() == i / 10);
    }
}

TEST_CASE("dataclasses/cell: test forEachMicrocell", "[Cell]")
{
    Cell subject = Cell(0);
    std::set<Microcell *> microcells;
    for (size_t i = 0; i < 100; i++)
    {
        subject.microcells().push_back(Microcell(i));
    }
    for (size_t i = 0; i < 100; i++)
    {
        microcells.insert(&subject.microcells()[i]);
    }
    REQUIRE(subject.microcells().size() == 100);
    REQUIRE(microcells.size() == 100);

    REQUIRE_NOTHROW(
        subject.forEachMicrocell(
            [&](Microcell *microcell)
            {
                REQUIRE(microcells.find(microcell) != microcells.end());
                microcells.erase(microcell);
                return true;
            }));
    REQUIRE(microcells.size() == 0);
}

TEST_CASE("dataclasses/cell: test forEachMicrocell early stop", "[Cell]")
{
    Cell subject = Cell(0);
    std::set<Microcell *> microcells;
    for (size_t i = 0; i < 100; i++)
    {
        subject.microcells().push_back(Microcell(i));
    }
    for (size_t i = 0; i < 100; i++)
    {
        microcells.insert(&subject.microcells()[i]);
    }
    REQUIRE(subject.microcells().size() == 100);
    REQUIRE(microcells.size() == 100);

    int ctr = 0;
    REQUIRE_NOTHROW(
        subject.forEachMicrocell(
            [&](Microcell *microcell)
            {
                REQUIRE(microcells.find(microcell) != microcells.end());
                microcells.erase(microcell);
                ctr++;
                return ctr < 50;
            }));
    REQUIRE(microcells.size() == 50);
}

TEST_CASE("dataclasses/cell: test forEachPerson", "[Cell]")
{
    Cell subject = Cell(0);
    std::set<Person*> people;
    subject.people().reserve(1000);
    for (size_t i = 0; i < 1000; i++)
    {
        subject.people().push_back(Person(0, i, 0));
        people.insert(&subject.people()[i]);
    }
    REQUIRE(subject.people().size() == 1000);
    REQUIRE(people.size() == 1000);

    REQUIRE_NOTHROW(
        subject.forEachPerson(
            [&](Person* person)
            {
                REQUIRE(people.find(person) != people.end());
                people.erase(person);
                return true;
            }));
    REQUIRE(people.size() == 0);
}

TEST_CASE("dataclasses/cell: test forEachPerson early stop", "[Cell]")
{
    Cell subject = Cell(0);
    std::set<Person*> people;
    subject.people().reserve(1000);
    for (size_t i = 0; i < 1000; i++)
    {
        subject.people().push_back(Person(0, i, 0));
        people.insert(&subject.people()[i]);
    }
    REQUIRE(subject.people().size() == 1000);
    REQUIRE(people.size() == 1000);

    int ctr = 0;
    REQUIRE_NOTHROW(
        subject.forEachPerson(
            [&](Person* person)
            {
                REQUIRE(people.find(person) != people.end());
                people.erase(person);
                ctr++;
                return ctr < 500;
            }));
    REQUIRE(people.size() == 500);
}

TEST_CASE("dataclasses/cell: test queue people", "[Cell]")
{
    CellPtr subject = makeSubject(10, 100);

    std::set<size_t> queued = std::set<size_t>();
    // Queue random set of people
    for (int i = 0; i < 1000; i++)
    {
        size_t p = static_cast<unsigned long>(std::rand() % 1000);
        // If person is already in queue, this returns false and person isn't added to queue
        REQUIRE((queued.find(p) == queued.end()) == subject->enqueuePerson(p));
        queued.insert(p);
    }

    // Check can't queue same person multiple times
    for (auto it = queued.begin(); it != queued.end(); it++)
    {
        REQUIRE(subject->enqueuePerson(*it) == false);
    }

    auto process = [&](size_t p)
    {
        REQUIRE(queued.find(p) != queued.end());
        queued.erase(p);
    };

    auto processNone = [&](size_t)
    {
        // Require this function is never called
        REQUIRE(1 == 2);
    };

    REQUIRE_NOTHROW(subject->processQueue(process)); // Process queue
    REQUIRE(queued.empty());
    REQUIRE_NOTHROW(subject->processQueue(processNone)); // Queue should have been cleared
    REQUIRE(queued.empty());
}

TEST_CASE("dataclasses/cell: test infectious grouping", "[Cell]")
{
    for (int rep = 0; rep < 100; rep++)
    {
        CellPtr subject = makeSubject(10, 100);
        REQUIRE_NOTHROW(subject->initializeInfectiousGrouping());
        REQUIRE_NOTHROW(subject->numDead());
        REQUIRE_NOTHROW(subject->numRecovered());
        REQUIRE_NOTHROW(subject->numInfectious());
        REQUIRE_NOTHROW(subject->numExposed());
        REQUIRE_NOTHROW(subject->numSusceptible());
        std::set<size_t> infectious;

        auto verifyInfectious = [&]()
        {
            std::set<size_t> tmp = std::set<size_t>(infectious);
            subject->forEachInfectious(
                [&](Person *p)
                {
                    REQUIRE(tmp.find(p->cellPos()) != tmp.end());
                    tmp.erase(p->cellPos());
                    return true;
                });
            REQUIRE(tmp.size() == 0);
        };

        auto verifyNonInfectious = [&]()
        {
            std::set<size_t> tmp = std::set<size_t>();
            for (size_t i = 0; i < subject->people().size(); i++)
                if (infectious.find(i) == infectious.end())
                    tmp.insert(i);

            subject->forEachNonInfectious(
                [&](Person *p)
                {
                    REQUIRE(tmp.find(p->cellPos()) != tmp.end());
                    tmp.erase(p->cellPos());
                    return true;
                });
            REQUIRE(tmp.size() == 0);
        };

        for (int cycle = 0; cycle < 10; cycle++)
        {

            for (int n = 0; n < 1000; n++)
            {
                size_t i = static_cast<size_t>(std::rand() % 1000);
                REQUIRE(subject->markInfectious(i) == (infectious.find(i) == infectious.end()));
                infectious.insert(i);
                REQUIRE(subject->numInfectious() == infectious.size());
            }

            REQUIRE_NOTHROW(verifyInfectious());
            REQUIRE_NOTHROW(verifyNonInfectious());

            for (int n = 0; n < 1000; n++)
            {
                size_t i = static_cast<size_t>(std::rand() % 1000);
                REQUIRE(subject->markNonInfectious(i) == (infectious.find(i) != infectious.end()));
                infectious.erase(i);
                REQUIRE(subject->numInfectious() == infectious.size());
            }

            REQUIRE_NOTHROW(verifyInfectious());
            REQUIRE_NOTHROW(verifyNonInfectious());
        }
    }
}

TEST_CASE("dataclasses/cell: test infectious sampling", "[Cell]")
{
    CellPtr subject = makeSubject(10, 100);
    subject->initialize();
    Person* infector;
    auto callback = [&](Person* p) { infector = p; return true; };
    std::mt19937_64 rg;
    REQUIRE_FALSE(subject->sampleInfectious(1, callback, rg));

    auto callback2 = [&](Person* p){
        subject->markInfectious(p->cellPos()); 
        p->updateStatus(subject.get(), InfectionStatus::InfectASympt, 1);
        return true;
    };
    REQUIRE(subject->sampleSusceptible(10, callback2, rg));
    REQUIRE(subject->sampleInfectious(5, callback, rg));
}

TEST_CASE("dataclasses/cell: test susceptible sampling", "[Cell]")
{
    CellPtr subject = makeSubject(10, 100);
    subject->initialize();
    CellPtr empty = makeSubject(10, 0);
    empty->initialize();

    Person* infector;
    std::mt19937_64 rg;
    auto callback = [&](Person* p) { infector = p; return true; };
    REQUIRE(subject->sampleSusceptible(1, callback, rg));
    REQUIRE_FALSE(empty->sampleSusceptible(1, callback, rg));
}

TEST_CASE("dataclasses/cell: test compartment counter", "[Cell]")
{
    CellPtr subject = makeSubject(10, 100);
    REQUIRE_NOTHROW(subject->initialize());
    REQUIRE(subject->compartmentCount(InfectionStatus::Susceptible) == 1000);
    REQUIRE(subject->microcells()[0].compartmentCount(InfectionStatus::Susceptible) == 100);
    REQUIRE(subject->compartmentCount(InfectionStatus::Exposed) == 0);
    REQUIRE(subject->microcells()[0].compartmentCount(InfectionStatus::Exposed) == 0);
}

TEST_CASE("dataclasses/cell: test set and get location", "[Cell]")
{
    Cell subject = Cell(0);
    auto base_loc = std::make_pair(0.0, 0.0);
    auto loc = std::make_pair(1.0, 1.0);
    REQUIRE(subject.location() == base_loc); //should work, might initialise to different values

    subject.setLocation(loc);
    REQUIRE_FALSE(subject.location() == base_loc);
    auto retrieve_loc = subject.location();
    REQUIRE(retrieve_loc == loc);
}

