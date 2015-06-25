#!/usr/bin/env python
# ----------------------------------------------------------------------------*
# imageBatch.py
#
# June 2011
#
# Perform operations on a specified folder of photos.
# Operations include rotating and equalizing. See
# http://www.pythonware.com/library/pil/handbook/
# for other possible operations.
#
# Requires Python Image Library (PIL):
# http://www.pythonware.com/products/pil/
#
# See http://www.instructables.com/member/aspro648/
# for more detailed instructions.

# FFMPEG to convert to movie
# ffmpeg -f image2 -r 1/5 -i image%05d.png -vcodec mpeg4 -y movie.mp4
# OR
# avconv -f image2 -i figMatplotlib%d.png -r 76 -s 800x600 foo.avi


import getopt, Image, ImageDraw, ImageEnhance, ImageFont, ImageOps, os, sys, time
from PIL.ExifTags import TAGS


def usage():
    '''Displays help'''

    print '''
    "imageBatch.py" performs specified operations on a folder of images in a batch.
    This is usefull for manipulating photos for timelapse sequences.

    Options:
       -h   --help       : displays this help message
       -d   --directory  : directory, relative to this file, where the photos
                           are located (omit if in same directory)
       -e   --equalize   : equalize image contrast
       -r   --rotation   : degrees to rotate (+ = ccw, - = cw)
       -c   --contrast   : contrast factor (1.0 = unchanged)
       -b   --brightness : brightness factor (1.0 = unchanged)
       -s   --sharpness  : sharpness factor (1.0 = unchanged)
       -t   --timestamp  : add file created time to images

       
    Example:
        "python ./photos.py -d myPictures -e -r -90 -b 1.5"
        will take all image files in "/myPictures", equalize contrast,
        rotate counter-clockwise 90 degress, brighten, and save to folder
        "myPictures/modified".
        
    Author:
        Ken Olsen, 648.ken@gmail.com

    '''


def ops(directory, rotation, equalize, contrast, brightness, sharpness, timestamp):
    ''' perform batch operations on a folder of images'''

    operations = ''
    if rotation: operations = operations + ' rotation=%s' % rotation
    if equalize: operations = operations + ' equalize=%s' % equalize
    if contrast: operations = operations+ ' contrast=%s' % contrast
    if brightness: operations = operations + ' brightness=%s' % brightness
    if sharpness: operations = operations + ' sharpness=%s' % sharpness

    if operations == '':
        print 'Nothing to do? Please specify the operations'
        usage()
        exit()
    else:
        print "Operations: ", operations

    filesModified = 0 
    modifiedDir = os.path.join(directory, 'modified')
    if not os.path.exists(modifiedDir): os.mkdir(modifiedDir)

    fileTypes = ['jpg', 'bmp', 'png', 'gif']
 
    for fileName in os.listdir(directory):
        splitName = fileName.rsplit('.', 1)
        if len(splitName) > 1:
            fileType = splitName[1]
            if fileType.lower() in fileTypes:
                fileHandle = os.path.join(directory, fileName) 
                im = Image.open(fileHandle)
                #im = ImageOps.autocontrast(im, cutoff=50)
                #im = ImageOps.posterize(im, 2)
                #im = ImageOps.invert(im)
                #im = ImageOps.solarize(im, 128)

                if rotation: im = im.rotate(rotation)
                if equalize: im = ImageOps.equalize(im)
                if contrast:
                    enh = ImageEnhance.Contrast(im)
                    im = enh.enhance(contrast)
                if brightness:
                    enh = ImageEnhance.Brightness(im)
                    im = enh.enhance(brightness)
                if sharpness:
                    enh = ImageEnhance.Sharpness(im)
                    im = enh.enhance(sharpness)                    
                newFile = os.path.join(modifiedDir, fileName)
                if timestamp:
                    offset = 7 * 60 * 60 #GMT to PST in seconds?
                    t = time.localtime(os.path.getctime(fileHandle)) #created
                    t = time.localtime(os.path.getmtime(fileHandle) - offset) #modified
                    stamp = time.strftime('%H:%M:%S', t)
                    font = ImageFont.truetype('ARIAL.TTF', 120)
                    canvas = Image.new("RGBA", (480, 120), (0,0,0,0))
                    txt = ImageDraw.Draw(canvas)
                    txt.text((0, 0), stamp, font=font, fill='#ff0000')
                    canvas.save("canvas2.png", "PNG")
                    im.paste(canvas, (15,10), canvas)
                #im = im.convert('L') # convert to b&W               
                im.save(newFile)
                filesModified += 1
                print '%s\t%s --> %s rot=%s' % (filesModified, fileName, newFile, rotation)
   
    print '\nDone! %s files saved in "%s".' % (filesModified, os.path.join(os.getcwd(), modifiedDir))
    print 'Operations: %s' % operations


def main():
    ''' parse arguments and execute operations '''
    
    try: 
        opts, args = getopt.getopt(sys.argv[1:], 'hed:r:c:b:s:t',
                                   ['help', 'dir=', 'equalize=', 'rotation=', 'contrast=',
                                    'brightness=', 'sharpness=', 'timestamp'])
    except getopt.GetoptError, err: # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    directory = 'commute'
    rotation = 90
    equalize = False
    contrast = False
    brighten = 1.5
    sharpen = 1.0
    timestamp = False

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        if o in ('-d', '--dir'):
            directory = a
        if o in ('-r', '--rotation'):
            rotation = float(a)
        if o in ('-e', '--equalize'):
            equalize = True
        if o in ('-r', '--rotation'):
            rotation = float(a)
        if o in ('-c', '--contrast'):
            contrast = float(a)
        if o in ('-b', '--brightness'):
            brighten = float(a)
        if o in ('-s', '--sharpness'):
            sharpen = float(a)
        if o in ('-t', '--timestamp'):
            timestamp = True
            
    ops(directory, rotation, equalize, contrast, brighten, sharpen, timestamp)


if __name__ == "__main__":
    main()

