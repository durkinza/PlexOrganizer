# Music organizer
# Author: Zane Durkin
# MusicOrganizer.py
# args:  -i  location_of_mp3s/
#        -o  output_location/
#        -G  organize by genre (genre must be in meta data)
# have all mp3 files in sigle folder, with album/artist in the meta data
# songs without meta data info will be placed in 'unkown' folder
# BIG THANKS TO stackoverflow.com
# get dependencies
import os
import sys
import getopt
import eyed3


def main(argv):
    # set global variables
    global inputfolder
    global outputfolder
    global genre
    # set default folder location to current directory
    inputfolder = '.'
    outputfolder = '.'
    # default genre organization to off
    genre = True
    # see if any file locations were given
    try:
        opts, args = getopt.getopt(argv, "hi:o:G", ["ifile=", "ofile="])
    except getopt.GetoptError:
        # if the arguments given created an error, output the help
        print 'test.py -i <inputfolder> -o <outputfolder> [-G (organize by genre)]'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            # print help
            print 'MusicOrganizer.py -i <inputfolder> -o <outputfolder>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            # overwrite the default file location if one was given
            inputfolder = arg
        elif opt in ("-o", "--ofile"):
            # overwrite the default output location if on was given
            outputfolder = arg
        elif opt in (""):
            genre = False
if __name__ == "__main__":
    main(sys.argv[1:])


def mp3gen():
    # get all mp3 files in given directory
    for root, dirs, files in os.walk(inputfolder):
        for filename in files:
            if os.path.splitext(filename)[1] == ".mp3":
                yield os.path.join(filename)

# for each mp3file found, get meta data
unorg_mp3s = []
# print 'Found: '
for mp3file in mp3gen():
    # print mp3file
    unorg_mp3s.append(mp3file)

# create base folder for music
baseFolder = outputfolder+"/Music"
if len(unorg_mp3s) > 0:

    # try to make base folder if it doesn't already exist
    try:
        if not os.path.exists(inputfolder+baseFolder):
            # if folder doesn't already exist, make it
            os.makedirs(inputfolder+baseFolder)
    except os.error:
        # if folder cannot be made, give error
        print 'Error: could not create folder(s).'
        print 'Maybe try running with elevated permissions?'
        sys.exit(1)
else:
    # if no mp3 files are found in the given folder
    print 'No mp3 files found'
    # if another directory hasn't been specified, offer a solution
    if inputfolder == '.':
        print 'Try \'MusicOrganizer.py -i <inputfolder>\' if files are in another directory'
    # exit without error
    sys.exit(0)

# start moving files to their folder(s)
for mp3file in unorg_mp3s:
    # print file that is being used
    print "moving: "+mp3file
    # load song to get info
    song = eyed3.load(inputfolder+'/'+mp3file)
    # tell song artist
    print song.tag.artist
