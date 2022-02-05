#include "covidsim.hpp"
#include "dataclasses/cell.hpp"
#include "dataclasses/person.hpp"

#include "catch/catch.hpp"

using namespace epiabm;

TEST_CASE("covidsim: test CalcHouseInf")
{
    Person subject = Person(0, 0, 0) ;
    unsigned short int timestep = 0;
    REQUIRE(Covidsim::CalcHouseInf(&subject, timestep) >= 0);
}

TEST_CASE("covidsim: test CalcCellInf")
{
    Cell subject = Cell(0);
    unsigned short int timestep = 0;
    REQUIRE(Covidsim::CalcCellInf(&subject, timestep) >= 0);

    // Add people to check exact value of function
    std::set<Person*> people;
    subject.people().reserve(10);
    for (size_t i = 0; i < 10; i++)
    {
        subject.people().push_back(Person(0, i, 0));
        people.insert(&subject.people()[i]);
    }
    subject.forEachPerson(
        [&](Person* person)
        {
            (*person).updateStatus(&subject, InfectionStatus::InfectMild, 0);
        });
    
    subject.initializeInfectiousGrouping();
    REQUIRE(Covidsim::CalcCellInf(&subject, timestep) == 20);
    // Should be R Value (2) * Number of infectious individuals
}

TEST_CASE("covidsim: test CalcSpaceInf")
{
    Cell subject = Cell(0);
    Person infector = Person(0, 0, 0) ;
    unsigned short int timestep = 0;
    REQUIRE(Covidsim::CalcSpaceInf(&subject, &infector, timestep) >= 0);
}

TEST_CASE("covidsim: test CalcHouseSucs")
{
    Person infector = Person(0, 0, 0) ;
    Person infectee = Person(0, 0, 0) ;
    unsigned short int timestep = 0;
    REQUIRE(Covidsim::CalcHouseSusc(&infector, &infectee, timestep) >= 0);
}

TEST_CASE("covidsim: test CalcPersonSucs")
{
    Person infector = Person(0, 0, 0) ;
    Person infectee = Person(0, 0, 0) ;
    unsigned short int timestep = 0;
    REQUIRE(Covidsim::CalcPersonSusc(&infector, &infectee, timestep) >= 0);
}

TEST_CASE("covidsim: test CalcSpaceSusc")
{
    Cell subject = Cell(0);
    Person infectee = Person(0, 0, 0) ;
    unsigned short int timestep = 0;
    REQUIRE(Covidsim::CalcSpaceSusc(&subject, &infectee, timestep) >= 0);
}

