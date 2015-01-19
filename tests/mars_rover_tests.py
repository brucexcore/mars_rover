#!/usr/bin/python

"""
Contains the test class for the Mars Rover project, which uses python's unittest
framework.

To execute all tests run mars_rover_tests.py or for the unittest help message
run with -h.
"""

__author__ = 'Bruce MacKenzie'

import unittest
import sys

sys.path.append( '../lib' )
from mars_rover import Planet
from mars_rover import Rover
from common import Point


class PlanetRoverTest( unittest.TestCase ):
    """The base class for test classes for the Mars Rover app.  Provides common
test data for implementing subclasses, initialized in setUp() when called by
unittest.main()."""

    def setUp( self ):
        self.negativePoint1 = Point( 1, -10 )
        self.negativePoint2 = Point( 1, -1 )
        self.zeroPoint = Point( 1, 0 )
        self.marsSize = Point( 10, 10 )
        self.mars = Planet( self.marsSize )  # init here since used by both subclasses(?)

        # invalid test data
        self.outOfBounds = Point( 11, 10 )


class PlanetTest( PlanetRoverTest ):
    """Test the Planet class with a variety of valid and invalid dimensions.
Input data is inherited from the parent."""

    def testValid( self ):
        """Test the Planet class with valid inputs"""
        self.assertEqual( self.marsSize, self.mars.size )


    def testInvalid( self ):
        """Test the Planet class with various invalid inputs"""
        self.assertRaises( ValueError, Planet, self.negativePoint1 )
        self.assertRaises( ValueError, Planet, self.negativePoint2 )
        self.assertRaises( ValueError, Planet, self.zeroPoint )


class RoverTest( PlanetRoverTest ):
    """Test the Rover class with a variety of valid and invalid paramters.
Input data is inherited from the parent."""

    def setUp( self ):
        super( RoverTest, self ).setUp( )  # inherit parent members
        self.startPos = Point( 1, 2 )
        self.endPos = Point( 1, 3 )
        self.startDir1 = 'N'
        self.moves1 = 'LMLMLMLMM'
        self.startDir2 = 'E'
        self.moves2 = 'MMMMMMMMMMM'
        self.endPos2 = Point( 10, 2 )
        self.endPos3 = Point( 10, 0 )
        self.rover = Rover( self.mars, self.startPos, \
                            self.startDir1, self.moves1 )

        # invalid test data
        self.invalidDir = 'D'
        self.invalidMoves = 'LMDMLMLMM'


    def testValid( self ):
        """Test the Rover class with valid inputs"""
        self.assertEqual( self.rover.planet, self.mars )
        self.assertEqual( self.rover.pos, self.startPos )
        self.assertEqual( self.rover.dir, self.startDir1 )
        self.assertEqual( self.rover.moves, self.moves1 )


    def testInvalid( self ):
        """Test the Rover class with various invalid inputs"""
        self.assertRaises( ValueError, Rover, *[self.mars, self.negativePoint1, \
                           self.startDir1, self.moves1] )
        self.assertRaises( ValueError, Rover, *[self.mars, self.negativePoint2, \
                           self.startDir1, self.moves1] )
        self.assertRaises( ValueError, Rover, *[self.mars, self.outOfBounds, \
                           self.startDir2, self.moves1] )
        self.assertRaises( ValueError, Rover, *[self.mars, self.startPos, \
                           self.invalidDir, self.moves1] )
        self.assertRaises( ValueError, Rover, *[self.mars, self.startPos, \
                           self.startDir2, self.invalidMoves] )


    def testMoves( self ):
        """Test the Rover class applyMoves() method"""
        self.assertEqual( self.endPos, self.rover.applyMoves() )

        # Test moves that attempt to go past the boundaries
        rover = Rover( self.mars, self.startPos, self.startDir2, self.moves2 )
        self.assertEqual( self.endPos2, rover.applyMoves() )
        rover.dir = 'S'
        self.assertEqual( self.endPos3, rover.applyMoves() )


if __name__ == '__main__':
    sys.exit( unittest.main() )
