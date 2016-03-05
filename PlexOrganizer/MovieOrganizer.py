# Movie Organizer
# Author: Zane Durkin
# MovieOrganizer.py
# args: -i location of movies
#       -o output location
#       -s make output folder the same as the input folder
#       -k keep files after moving
# Have all movies in single folder

import os
import sys
import re
import getopt
from __init__ import __version__ as version
import shutil

help = """
MovieOrganizer

    Usage:
        MovieOrganizer.py [-i <inputFolder>][-o <outputFolder>][-sk]
    Options:
        -v          --version
        -i <path>   --inputFolder=<path>    [Default: '.']
        -o <path>   --outputFolder=<path>   [Default: '.']
        -s          --same                  [set output folder to the same as input (overrrides --outputFolder)]
        -k          --keep                  [Keep original files in their starting folder (copies instead of moving)]
        -y                                  [Don't ask to overwrite files]
"""


def main(argv):
    # set global variables
    global inputFolder
    global outputFolder
    global remove
    global sameFolder
    global ask
    # set defaults
    remove = True
    sameFolder = False
    ask = True
    inputFolder = '.'
    outputFolder = '.'
    try:
        opts, args = getopt.getopt(argv, "hi:o:yskv", ["inputFolder=", "outputFolder=", "same", "keep", "genre", "version"])
    except getopt.GetoptError:
        # if the arguments given created an error, output the help
        print 'test.py -i <inputfolder> [-o <outputfolder> [-h for more help]'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            # print help
            print help
            sys.exit()
        elif opt in ("-i", "--inputFolder"):
            # overwrite the default file location if one was given
            inputFolder = arg
        elif opt in ("-o", "--outputFolder"):
            # overwrite the default output location if on was given
            outputFolder = arg
        elif opt in ('-k', '--keep'):
            remove = False
        elif opt in ('-s', '--same'):
            sameFolder = True
        elif opt in ('-v', '--verison'):
            print version
            sys.exit(2)
        elif opt in ('-y'):
            ask = False
    if(sameFolder):
        outputFolder = inputFolder

    # create an array of movies
    unorg_movies = []

    for movie in moviegen():
        unorg_movies.append(movie)

    if len(unorg_movies) > 0:
        baseFolder = outputFolder
        # create Media folder, if it doesn't exit
        if not os.path.exists(baseFolder+'/Media'):
            # if folder doesn't exist, create it
            try:
                os.makedirs(baseFolder+'/Media')
                baseFolder = baseFolder+'/Media'
            except os.error:
                # if folder cannot be made, give error
                print 'Error: could not create folder(s) in output folder.'
                print 'Maybe try running with elevated permissions?'
                sys.exit(1)
        else:
            baseFolder = baseFolder+'/Media'
        # create base folder for movies to be moved to
        if not os.path.exists(baseFolder+'/Movies'):
            # if folder doesn't exist, make it
            try:
                os.makedirs(baseFolder+'/Movies')
                baseFolder = baseFolder+'/Movies'
            except os.error:
                # if folder cannot be made
                print 'Error: could not create folder(s) in output folder.'
                print 'Maybe try running with elevated permissions?'
                sys.exit(1)
        else:
            baseFolder = baseFolder+'/Movies'
    else:
        # if no files are found
        print 'No movie files found'
        if inputFolder == '.':
            print 'Try \'MovieOrganizer.py -i <inputFolder>\' if files are in another directory'
        # exit without error
        sys.exit(0)

    # start working on moving the movies over
    for movie in unorg_movies:
        print 'Working on: '+movie
        tmp_baseFolder = str(baseFolder).encode('ascii')
        # get movie folder name
        movie_folder = os.path.splitext(movie)[0]
        # try to create the folder
        try:
            # try to create movie folder if doesn't exist
            if not os.path.exists(tmp_baseFolder+'/'+movie_folder):
                os.makedirs(tmp_baseFolder+'/'+movie_folder)
        except os.error:
            # if the folder cannot be made
            print 'Error: could not create folder(s) in output folder.'
            print 'Maybe try running with elevated permissions?'
            sys.error(1)
        # added movie folder to the basefoder
        tmp_baseFolder = tmp_baseFolder+'/'+movie_folder
        # flag to keep from overwriting current files
        flag = False
        # see if the movie exists
        if os.path.exists(tmp_baseFolder+'/'+movie):
            # if the movie exists, ask to overwrite
            if ask:
                # if should ask, get input
                if raw_input(movie+" already exists. overwrite?: [Y/n]") in ('N', 'n', None, ''):
                    continue
                else:
                    flag = True
            else:
                flag = True
        else:
            flag = True
        # try to move movie
        try:
            # if flag is true (means it is ok to overwrite)
            if(flag):
                # if the user wants to keep original files
                if(remove):
                    # remove the file while transfering
                    print 'Moving '+inputFolder+'/'+movie+' To '+tmp_baseFolder+'/'+movie
                    try:
                        os.rename(inputFolder+'/'+movie, tmp_baseFolder+'/'+movie)
                    except os.error:
                        # if the movie could not be moved
                        print 'Error: Could not move file to directory'
                        sys.exit(1)
                else:
                    # keep the file after transfering
                    print 'Copying '+inputFolder+'/'+movie+' to '+tmp_baseFolder+'/'+movie
                    try:
                        shutil.copy(inputFolder+'/'+movie, tmp_baseFolder+'/'+movie)
                    except shutil.Error:
                        print 'Error: Could not move file to directory'
                        sys.exit(1)
        except os.error:
            print 'Error: could not create folder(s) in output folder.'
            print 'Maybe try running with elevated permissions?'
            sys.error(1)


def moviegen():
    # get all mp3 files in given directory
    for root, dirs, files in os.walk(inputFolder):
        for filename in files:
            if os.path.splitext(filename)[1] in ('.mp4', '.mov', '.avi', '.mov', '.m4v', '.mpeg'):
                yield os.path.join(filename)


if __name__ == "__main__":
    # start main function
    main(sys.argv[1:])
