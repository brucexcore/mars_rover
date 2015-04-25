#!/usr/bin/python

"""The Mars Rover application main module.  Run with no arguments for run
instructions.
"""

# ToDo:
#   - readme file
#   - purge all (?)
#   - verify docstrings by displaying in interactive session
#   - test rover against wall

__author__ = 'Bruce MacKenzie'

import sys
import os

from common import Point


class Planet( object ):
    """The planet class represents a plateau on a planet as a two dimensional
grid.  The lower-left corner is 0,0 and the upper-right is the x,y values
provided.  Note that because both 0 and x/y are cells the length and width of
the grid are actually x+1 and y+1."""

    def __init__( self, size ):
        """Initializes a Planet object.  size is a named tuple called a point,
defined in common.py.  Performs error checking and raises ValueError if an
invalid parameter is encountered."""

        if size.x < 1 or size.y < 1:
            raise ValueError( 'Dimensions not positive numbers' )
        self.size = size



class Rover( object ):
    """The Rover class represents a rover that has landed on a planet."""

    validDirs = [ 'N', 'E', 'S', 'W' ]
    validMoves = [ 'L', 'R', 'M' ]

    # These dictionaries act as lookup tables for the different moves to avoid
    # the use of many if statements in determining moves
    _directions = { 'N': {'L':'W', 'R':'E'}, \
                    'E': {'L':'N', 'R':'S'}, \
                    'S': {'L':'E', 'R':'W'}, \
                    'W': {'L':'S', 'R':'N'} }
    _moveIncrements = { 'N':1, 'E':1, 'S':-1, 'W':-1 }


    def __init__( self, planet, startPos, startDir, moves ):
        """Initializes a Rover object.  Takes the following parameters:

- planet is a Planet object this rover has landed on.
- startPos is the starting position on the planet.  It is a named tuple called a
  Point, defined in common.py.
- startDir is the initial direction the rover is facing, it may be one of the
  four cardinal compass positions, represented as one of 'N', 'E', 'S', 'W'.
- moves is a string of moves the rover will make when applyMoves() is called.
  Each character may be 'L' or 'R' to rotate the rover 90 degrees left or right,
  respectively, or 'M' to move one position in the direction it is facing.

Performs error checking and raises ValueError if an invalid parameter is
encountered."""

        # Input validation
        if startPos.x < 1 or startPos.y < 1:
            raise ValueError( 'Dimensions not positive numbers: ' + \
                              str(startPos) )
        if startPos.x > planet.size.x or startPos.y > planet.size.y:
            raise ValueError( 'Dimensions greater than planet size: ' + \
                              'start position: ' + str(startPos) + ' ' + \
                              'planet size: ' + str(planet.size) )
        if not startDir in self.validDirs:
            raise ValueError( 'Start direction not valid: ' + startDir )
        for m in moves:
            if not m in self.validMoves:
                raise ValueError( 'Move not valid: ' + m + ' in ' + str(moves) )

        self.planet = planet
        self.pos = startPos
        self.dir = startDir
        self.moves = moves


    def applyMoves( self ):
        """Apply the moves in self.moves and return the final position as a
Point object.  If the rover is against an edge and tries to move in that
direction it will stay in that spot."""

        for m in self.moves:
            if m != 'M':
                self.dir = self._directions[self.dir][m]
            else:
                if self.dir == 'N' or self.dir == 'S':
                    newYPos = self.pos.y + self._moveIncrements[self.dir]
                    if newYPos >= 0 and newYPos <= self.planet.size.y:
                        self.pos = Point( self.pos.x, newYPos )
                else:  # moving E or W
                    newXPos = self.pos.x + self._moveIncrements[self.dir]
                    if newXPos >= 0 and newXPos <= self.planet.size.x:
                        self.pos = Point( newXPos, self.pos.y )

        return self.pos



class MissionControl( object ):
    """A class representing the NASA mission control centre operating the
rovers."""

    def __init__( self, inputFile ):
        """Initializes a mission control object.  Input file is read in and
the Planet and Rover objects are created with this data."""

        # Read input file
        inputLines = open( inputFile ).readlines( )
        if len(inputLines) < 3:
            raise ValueError( 'Input file incomplete: ' + inputFile )

        # Parse planet data
        inputLines[0] = inputLines[0].rstrip()
        sizes = inputLines[0].split(' ')
        # Check line containing initial position information is correct
        if len(sizes) < 2 or not sizes[0].isdigit() or not sizes[1].isdigit():
            raise ValueError( 'Input file format invalid, line: ' + \
                              inputLines[0] )
        self.mars = Planet( Point(int(sizes[0]), int(sizes[1])) )

        # Parse each rover's data
        self.rovers = [ ]
        for i in range(1, len(inputLines), 2):
            # Check for at least two more lines in file
            if i+1 >= len(inputLines):
                raise ValueError( 'Input file incomplete: ' + inputFile )

            inputLines[i] = inputLines[i].rstrip( )
            inputLines[i+1] = inputLines[i+1].rstrip( )

            # Check line containing initial position information is correct
            initPos = inputLines[i].split(' ')
            if len(initPos) < 3 or not initPos[0].isdigit() or \
              not initPos[1].isdigit():
                raise ValueError( 'Input file format invalid, line: ' + \
                                  inputLines[i] )

            self.rovers.append( Rover(self.mars, Point(int(initPos[0]), \
                                      int(initPos[1])), initPos[2], \
                                      inputLines[i+1]) )


    def moveRovers( self ):
        """Move the rovers one at a time.  Prints the results to stdout."""

        for r in self.rovers:
            p = r.applyMoves( )
            print p.x, p.y, r.dir



def main( ):
    # Perform some basic input validation
    if len(sys.argv) < 2:
        print 'Run with the input file as a single argument:'
        print '\n\tpython mars_rover <input_file>\n'
        return 0

    if not os.path.exists( sys.argv[1] ):
        print 'Input file ' + sys.argv[1] + ' does not exist'
        return 1

    # Run the mars rover 
    try:
        mcc = MissionControl( sys.argv[1] )
        mcc.moveRovers( )
    except ValueError as e:
        print e.message + '\nsee README.md for more info on input data.\n'

    return 0


if __name__ == '__main__':
    sys.exit( main() )
