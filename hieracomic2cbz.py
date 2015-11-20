#!/usr/bin/python


import os,sys
import re
import shutil
import tempfile
import subprocess
import argparse

RE_PDF=re.compile('\.pdf$' , re.IGNORECASE)
RE_PPM=re.compile('\.ppm$')

def pdf2cbz(pdf, cbz):
	td=tempfile.mkdtemp(prefix='cbz-')
	wd=os.path.join(td,'here')
	pdfname=RE_PDF.sub('',os.path.basename(pdf))
	os.mkdir(wd)
	suffix_creation=os.path.join(wd,'page')
	ret=subprocess.check_call(['pdfimages', pdf, suffix_creation])
	if ret != 0:
		print 'extraction of pdf(%s) failed' % pdf
		sys.exit()
	for ppm in os.listdir(wd):
		ppmpath=os.path.join(wd,ppm)
		jpgpath=RE_PPM.sub('.jpg', ppmpath)
		ret=subprocess.check_call(['convert', ppmpath, jpgpath])
		if ret != 0:
			print 'ppm(%s) to jpg failed for pdf(%s)' % (ppmpath,pdf)
			sys.exit()
		os.remove(ppmpath)
	os.chdir(wd)
	tcbz=os.path.join(td,os.path.basename(cbz))
	print 'cd', wd
	if not len(os.listdir(wd)):
		print "this pdf does not contains images, skip it ! "
	else:
		print 'zip -q -r "%s" "./"' % tcbz
		ret=subprocess.check_call(['zip', '-q', '-r', tcbz, './'])
		if ret != 0:
			print 'zip(%s) failed to create from dir(%s)' %(tcbz, wd)
			sys.exit()
		print 'mv "%s" "%s"' % (tcbz, cbz)
		shutil.copy(tcbz, cbz)
		os.chdir(os.path.expanduser('~'))
	shutil.rmtree(td)




def src2dest(src, dst):
    force=False

    ltaff=[]
    for dirpath, ldirname, lfilename in os.walk(org):
	    for dirname in ldirname:
		    odirpath=os.path.join(dirpath,dirname)
		    ddirpath=odirpath.replace(org,dst)
		    if not os.path.isdir(ddirpath):
			    os.mkdir(ddirpath)
	    for filename in lfilename:
		    ofilepath=os.path.join(dirpath,filename)
		    dfilepath=ofilepath.replace(org,dst)
		    is_pdf=bool(RE_PDF.findall(ofilepath))
		    if (is_pdf and force):
			    print "forced ", ofilepath
			    cbz=RE_PDF.sub('.cbz', dfilepath)
			    ltaff.append([ofilepath, cbz])
			    continue
		    elif is_pdf:
			    cbz=RE_PDF.sub('.cbz', dfilepath)
			    if not os.path.isfile(cbz):
				    ltaff.append([ofilepath, cbz])
		    else:
			    if not os.path.isfile(dfilepath):
				    shutil.copyfile(ofilepath,dfilepath)


    len_taff=len(ltaff)
    i=0
    for taff in ltaff:
        i=i+1
        pdf,cbz=taff
        print "job %s/%s" % (i,len_taff)
        print 'convert pdf( "%s" ):' % pdf
        print '     to cbz( "%s" )' % cbz
        pdf2cbz(pdf,cbz)
        print ''

if "__main__" == __name__:
    parser = argparse.ArgumentParser(description='Construct a copy of a hierarchy, and convert every pdf or cbr to cbz')
    parser.add_argument('src', metavar='source', type=str,
                       help='source can be either a file or a directory)
    parser.add_argument('dst', metavar='destination', type=str,
                       help='destination should be of the same type of source')
    parser.add_argument('--force-redo', dest='force_redo', action='store_true', default=False,
                       help='force to convert again the files')

    args = parser.parse_args()
	org="/home/briner/bd/"
	dst="/home/briner/cbz/"

