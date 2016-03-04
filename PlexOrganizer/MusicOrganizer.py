# Music organizer
# Author: Zane Durkin
# MusicOrganizer.py
# args:  -i  location_of_mp3s/
#        -o  output_location/
#        -G  organize by genre (genre must be in meta data)
#        -s  make output folder the same as the input folder
#        -k  keep files after moving
# have all mp3 files in sigle folder, with album/artist in the meta data
# songs without meta data info will be placed in 'unkown' folder
# BIG THANKS TO stackoverflow.com
# get dependencies
import os
import sys
import re
import getopt
import eyed3
import shutil

help = """
MusicOrganizer

    Usage:
        MusicOrganizer.py [-i <inputFolder>][-o <outputFolder>][-skG]
        MusicOrganizer.py
    Options:
        -i <path>   --inputFolder=<path>    [Default: '.']
        -o <path>   --outputFolder=<path>   [Default: '.']
        -s          --same                  [Set output to the same as input (overrides --outputFolder)]
        -k          --keep                  [Keep original mp3s in their starting foler (copies instead of moving)]
        -G          --genre                 [Order songs by genre and then by artist]

"""


def main(argv):
    # set global variables
    global inputFolder
    global outputFolder
    global genre
    global remove
    global sameFolder
    # set default folder location to current directory
    inputFolder = '.'
    outputFolder = '.'
    # default genre organization to off
    genre = False
    remove = True
    sameFolder = False
    # see if any file locations were given
    try:
        opts, args = getopt.getopt(argv, "hi:o:Gsk", ["inputFolder=", "outputFolder=", "same", "keep", "genre"])
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
        elif opt in ('-G', '--genre'):
            genre = True
        elif opt in ('-k', '--keep'):
            remove = False
        elif opt in ('-s', '--same'):
            sameFolder = True
    if(sameFolder):
        outputFolder = inputFolder

if __name__ == "__main__":
    main(sys.argv[1:])


def mp3gen():
    # get all mp3 files in given directory
    for root, dirs, files in os.walk(inputFolder):
        for filename in files:
            if os.path.splitext(filename)[1] == ".mp3":
                yield os.path.join(filename)

# for each mp3file found, get meta data
unorg_mp3s = []
# print 'Found: '
for mp3file in mp3gen():
    # print mp3file
    unorg_mp3s.append(mp3file)

if len(unorg_mp3s) > 0:
    baseFolder = outputFolder
    # create Media folder, if it doesn't exist
    try:
        if not os.path.exists(baseFolder+'/Media'):
            # if folder doesn't already exist, make it
            os.makedirs(baseFolder+'/Media')
            baseFolder = baseFolder+'/Media'
        else:
            baseFolder = baseFolder+'/Media'
    except os.error:
        # if folder cannot be made, give error
        print 'Error: could not create folder(s) in output folder.'
        print 'Maybe try running with elevated permissions?'
        sys.exit(1)

    # create base folder for music to be moved to
    baseFolder = baseFolder+"/Music"
    # try to make base folder if it doesn't already exist
    try:
        if not os.path.exists(baseFolder):
            # if folder doesn't already exist, make it
            os.makedirs(baseFolder)
    except os.error:
        # if folder cannot be made, give error
        print 'Error: could not create folder(s) in output folder.'
        print 'Maybe try running with elevated permissions?'
        sys.exit(1)
else:
    # if no mp3 files are found in the given folder
    print 'No mp3 files found'
    # if another directory hasn't been specified, offer a solution
    if inputFolder == '.':
        print 'Try \'MusicOrganizer.py -i <inputfolder>\' if files are in another directory'
    # exit without error
    sys.exit(0)

# start moving files to their folder(s)
for mp3file in unorg_mp3s:
    # print file that is being used
    print "Working on: "+mp3file
    # load song to get info
    song = eyed3.load(inputFolder+'/'+mp3file)
    tmp_baseFolder = str(baseFolder).encode('ascii')
    # if the songs should be ordered by genre aswell as artist
    if genre:
        # get the song genre
        song_genre = re.escape(str(song.tag.genre).encode('ascii'))
        # if the song has no genre, use the Unkown genre
        if (song_genre == '') or (song_genre == 'None'):
            song_genre = 'Unknown'
        print str('genre: '+song_genre)
        # change the temp basefolder if genre should be used
        tmp_baseFolder = str(baseFolder+'/'+song_genre).encode('ascii')
    # tell song artist
    song_artist = re.sub('[^\w\-_\. ]', '_', str(song.tag.artist).strip())
    # song_artist = re.escape(str(song.tag.artist).strip())
    # if the song has no artist, use the Unkown artist folder
    if (song_artist == '') or (song_artist == 'None'):
        song_artist = 'Unknown'
    print str('artist: '+song_artist)
    # create artist folder if not already made
    try:
        # try to create if it doesn't exist
        if not os.path.exists(tmp_baseFolder+'/'+song_artist):
            os.makedirs(tmp_baseFolder+'/'+song_artist)
    except os.error:
        # if the folder cannot be made
        print 'Error: Could not create sub-folder(s) in '+baseFolder+'/Music'
        sys.exit(1)
    if(remove):
        print 'Moving '+inputFolder+'/'+mp3file+' To '+baseFolder+'/'+song_artist
        try:
            os.rename(inputFolder+'/'+mp3file, baseFolder+'/'+song_artist+'/'+mp3file)
        except os.error:
            # the mp3 file could not be moved
            print 'Error: Could not move file to directory'
            sys.exit(1)
    else:
        print 'Copying'+inputFolder+'/'+mp3file+' To '+baseFolder+'/'+song_artist
        try:
            shutil.copy(inputFolder+'/'+mp3file, baseFolder+'/'+song_artist+'/'+mp3file)
        except shutil.Error:
            print 'Error: Could not move file to directory'
            sys.exit(1)
