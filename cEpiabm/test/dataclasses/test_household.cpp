
#include "dataclasses/household.hpp"
#include "dataclasses/microcell.hpp"
#include "dataclasses/cell.hpp"
#include "dataclasses/person.hpp"

#include <catch2/catch_test_macros.hpp>

#include <random>

using namespace epiabm;

inline Cell makeSubject(size_t n_microcells, size_t n_households, size_t n_people)
{
    Cell subject = Cell();
    subject.microcells().reserve(n_households);
    subject.people().reserve(n_microcells * n_people);
    for (size_t i = 0; i < n_microcells; i++)
    {
        subject.microcells().push_back(Microcell(i));
        subject.microcells()[i].people().reserve(n_people);
        subject.microcells()[i].households().reserve(n_households);
        for (size_t j = 0; j < n_households; j++)
        {
            subject.microcells()[i].households().push_back(Household(j));
        }
        for (size_t j = 0; j < n_people; j++)
        {
            subject.microcells()[i].people().push_back(subject.people().size());

            subject.people().push_back(
                Person(
                    subject.people().size(),
                    subject.microcells()[i].people().size() - 1));

            /*printf("Microcell: %ld, Person: (%ld, %ld)\n",
                i,
                subject.people()[subject.microcells()[i].people()[j]].cellPos(),
                subject.people()[subject.microcells()[i].people()[j]].microcellPos());//*/
        }
    }
    return subject;
}

TEST_CASE("dataclasses/household: test initialize household", "[Household]")
{
    Household subject = Household(5);
    REQUIRE(subject.microcellPos() == 5);
    REQUIRE_NOTHROW(subject.params());
}

TEST_CASE("dataclasses/household: test add member", "[Household]")
{
    Household subject = Household(5);
    REQUIRE(subject.microcellPos() == 5);
    REQUIRE_NOTHROW(subject.params());

    REQUIRE(subject.members().empty());

    std::set<size_t> members = std::set<size_t>();
    for (int i = 0; i < 100000; i++)
    {
        size_t newMember = static_cast<size_t>(std::rand() % 100000);
        REQUIRE(subject.addMember(newMember) == (members.find(newMember) == members.end()));
        members.insert(newMember);
    }

    for (size_t i = 0; i < 1000000; i++)
    {
        REQUIRE(subject.isMember(i) == (members.find(i) != members.end()));
    }
}

inline void forEachMemberTest(size_t n_microcells, size_t n_households, size_t n_people)
{
    std::vector<std::vector<std::set<Person *>>> members(
        n_microcells, std::vector<std::set<Person *>>(n_households));

    Cell subject = makeSubject(n_microcells, n_households, n_people);

    //std::cout << "Num Microcells: " << subject.microcells().size() << std::endl;
    for (size_t mc = 0; mc < subject.microcells().size(); mc++)
    {
        //std::cout << "Num People: " << subject.microcells()[mc].people().size() << std::endl;
        for (size_t p = 0; p < subject.microcells()[mc].people().size(); p++)
        {
            size_t hh = static_cast<size_t>(std::rand())%n_households;
            REQUIRE(subject.people()[subject.microcells()[mc].people()[p]]
                        .setHousehold(hh));
            REQUIRE(subject.microcells()[mc].households()[hh].addMember(p));
            members[mc][hh].insert(
                &subject.people()[subject.microcells()[mc].people()[p]]);
        }
    }

    for (size_t mc = 0; mc < subject.microcells().size(); mc++)
    {
        for (size_t hh = 0; hh < subject.microcells()[mc].households().size(); hh++)
        {
            auto callback = [&](Person *p)
            {
                REQUIRE(p->household() == hh);
                REQUIRE((members[mc][hh].find(p) == members[mc][hh].end()) == false);
                members[mc][hh].erase(p);
                return true;
            };

            REQUIRE_NOTHROW(subject.microcells()[mc].households()[hh].forEachMember(
                subject, subject.microcells()[mc], callback));

            REQUIRE(members[mc][hh].size() == 0);
        }
    }

    for (size_t mc = 0; mc < subject.microcells().size(); mc++)
    {
        for (size_t hh = 0; hh < subject.microcells()[mc].households().size(); hh++)
        {
            size_t ctr = 0;
            auto callback = [&](Person *p)
            {
                REQUIRE(members[mc][hh].find(p) == members[mc][hh].end());
                members[mc][hh].insert(p);
                ctr++;
                return (ctr < (n_people / 2));
            };

            REQUIRE_NOTHROW(subject.microcells()[mc].households()[hh].forEachMember(
                subject, subject.microcells()[mc], callback));

            REQUIRE(members[mc][hh].size() == ctr);
        }
    }
}

TEST_CASE("dataclasses/household: test forEachMember Small", "[Household]")
{
    forEachMemberTest(1, 1, 1000);
    forEachMemberTest(1, 10, 1000);
    forEachMemberTest(1, 100, 1000);
}

TEST_CASE("dataclasses/household: test forEachMember Medium", "[Household]")
{
    forEachMemberTest(2, 5, 10);
    forEachMemberTest(10, 10, 1000);
    forEachMemberTest(10, 1000, 5000);
}
