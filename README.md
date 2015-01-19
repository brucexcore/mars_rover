
Mars Rover Readme
=================

Written by: Bruce MacKenzie


Description
-----------
A squad of robotic rovers are to be landed by NASA on a plateau on Mars. This
plateau, which is curiously rectangular, must be navigated by the rovers so that
their on board cameras can get a complete view of the surrounding terrain to
send back to Earth.

See the input section on configuring the rovers.


Run Instructions
----------------
1. Run the app

From the mars_rover directory:

    python lib/mars_rover.py tests/test_inputs.txt
    
2. Run unit tests

First cd to mars_rover/tests.  mars_rover_tests.py must be run from here for its
imports to work.

The unit tests use Python's built-in unittest framework, which provides
convenient functionality such as a command line interface (CLI) and test
reports.

To run all tests:

    python mars_rover_tests.py

To run only tests for the Rover or Planet class:

    python mars_rover_tests.py [RoverTest|PlanetTest]

To run a specific test method in a test class:

    python mars_rover_tests.py <TestClass>.<testMethod>

For information on test methods see the interactive help or source code.  For
information on the test cases and various asserts see the source code.

For help on the unittest CLI:

    python mars_rover_tests.py --help


Input Data
--------------
An input file must contain as a minimum the following:

    5 5
    1 2 N
    LMRMLMLMM

The first line is the size of the plateau on mars the rover will land on.  It
must be at least 1 1, or a 2x2 grid so the rover has room to move.  Note a size
of 1 1 is 2x2 because 0,0 is the bottom-left coordinate.  It has been
(arbitrarily) decided the minimum size of a plateau is 1 1, or 2x2.

Each subsequent two lines denote a rover.  The first  is the rover's initial
position, which must be within the bounds of the plateau, and the direction
faced as a cardinal compass position (N, E, S, W).

The second line is a series of moves.  Each move must either be L or R
indicating a 90 degree turn, or M to move one step forward.  Don't worry if a
rover is against and facing a wall, a following M won't yield an error, the
rover simply won't move.  There can be any number and combination of moves, even
0.

The file may contain any number of rovers but each must have both lines.


Output
------
The output is the final position of each rover, printed on separate lines to
stdout.


Design Decisions
-----------
For low-level details see the docstrings, accessible via the interactive prompt:

    python -i
    >>> import mars_rover
    >>> help(mars_rover)
    >>> help(mars_rover.Rover)


Input
-----
It was decided input would be provided to the app via a filename passed as a
command line argument.  The file is read and parsed by MissionControl.

Unit test data is hard-coded into the mars_rover_tests.py module.


Error handling
--------------
Input is validated by each class's constructor by raising exceptions.  main()
will catch any exception raised and display it in a user-friendly manner, hiding
the backtrace.  Error handling is comprehensive.


Testing
-------
Python's unittest framework is used to test the Planet and Rover classes.  Each
test method contains a considerable number of asserts.  This may be overkill, 
but the prinicple is to convey proper testing of boundary cases, code coverage,
etc.

Testing the MissionControl class executes the whole system, and as a result
utilizes functional testing instead of unit testing.  It may be tested by
running mars_rover against the various test input files found in tests/.  These
tests are carried out manually but of course could easily be automated.  See
tests/functional_tests.txt for more information on these tests.


OO
--
The classes in mars_rover are designed to ensure low coupling and high cohesion.

The test classes make use of polymorphism to share common test data.

Encapsulation is not as stringently followed in Python as other languages such
as Java.  Private members can still be accessed from outside, and the main
purpose they serve is name scrambling to prevent being overridden by subclasses.
As a result most members are declared public, with the exception of some class
members in Rover defined with protected scope.  This follows the Python
philosophy "We're all consenting adults here".
