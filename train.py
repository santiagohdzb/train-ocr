#!\\usr\\bin\\python

from os import path
from os.path import join
import os
import glob
import sys

# country = raw_input("Two-Letter Country Code to Train: ").lower()
country = "eu"
CURRENT_DIR = os.getcwd()
TESSERACT_DIR = 'G:\\AB\\TCGAS\\DEMOS\\train-ocr\\tesseract'
TESSERACT_BIN = join(TESSERACT_DIR, "tesseract")
TEMP_DIR = join(CURRENT_DIR, "tmp")
TESSERACT_TRAINDIR = TESSERACT_DIR
LANGUAGE_NAME = 'l' + country

os.environ["TESSDATA_PREFIX"] = TESSERACT_DIR
box_files = glob.glob(join(CURRENT_DIR, country, "input", "") + "*.box")

if not box_files:
    print("Cannot find input files")
    sys.exit(1)
    
os.system('del /Q "%s"' % join(TEMP_DIR, "*"))
font_properties_file = open(join(TEMP_DIR, "font_properties"),'w')

BOX_FILES_LIST = ""
TR_FILES_LIST = ""

for box_file in box_files:
    print("Processing: " + box_file)

    file_without_dir = path.split(box_file)[1]
    file_without_ext = path.splitext(file_without_dir)[0]
    input_dir = path.dirname(box_file)
    tif_file = join(input_dir, file_without_ext + ".tif")
    train_cmd = '%s %s %s box.train.stderr' % (TESSERACT_BIN, tif_file, file_without_ext)

    print("Executing: " + train_cmd)
    os.system(train_cmd)

    output_tr = file_without_ext + ".tr"
    output_txt = file_without_ext + ".txt"

    if (path.exists(join(CURRENT_DIR, output_tr))):
        os.system("move %s %s" % (join(CURRENT_DIR, output_tr), join(TEMP_DIR, output_tr)))
    else:
        print("Train did not work as there is not output files")
        sys.exit(1)

    if (path.exists(join(CURRENT_DIR, output_txt))):
        os.system("move %s %s" % (join(CURRENT_DIR, output_txt), join(TEMP_DIR, output_txt)))

    font_name = file_without_dir.split('.')[1]
    font_properties_file.write(font_name + ' 0 0 1 0 0\n')

    BOX_FILES_LIST += '"' + box_file + '" '
    TR_FILES_LIST += '"' + join(TEMP_DIR, output_tr) + '" '

font_properties_file.close()

train_cmd = join(TESSERACT_TRAINDIR, "unicharset_extractor") + " " + BOX_FILES_LIST
print("Executing: " + train_cmd)
os.system(train_cmd)
os.system("move %s %s" % (join(CURRENT_DIR, "unicharset"), join(TEMP_DIR, LANGUAGE_NAME + ".unicharset")))

train_cmd = '%s -F "%s" -U unicharset -O "%s" %s' % (join(TESSERACT_TRAINDIR, "mftraining"), join(TEMP_DIR, "font_properties"), join(TEMP_DIR, LANGUAGE_NAME + ".unicharset"), TR_FILES_LIST)
print("Executing: " + train_cmd)
os.system(train_cmd)

if (path.exists(join(CURRENT_DIR, "unicharset"))):
    os.system("del " + join(CURRENT_DIR, "unicharset"))
if (path.exists(join(TEMP_DIR, LANGUAGE_NAME + ".unicharset"))):
    os.system("move " + join(TEMP_DIR, LANGUAGE_NAME + ".unicharset") + " " + CURRENT_DIR)
if (path.exists(join(CURRENT_DIR, country, "input", "unicharambigs"))):
    os.system("copy " + join(CURRENT_DIR, country, "input", "unicharambigs") + path.join(CURRENT_DIR, LANGUAGE_NAME + ".unicharambigs"))

train_cmd = join(TESSERACT_TRAINDIR, "cntraining") + ' ' + TR_FILES_LIST
print("Executing: " + train_cmd)
os.system(train_cmd)

if (path.exists(join(CURRENT_DIR, "shapetable"))):
    os.system("move %s %s" % (join(CURRENT_DIR, "shapetable"), join(CURRENT_DIR, LANGUAGE_NAME + ".shapetable")))
if (path.exists(join(CURRENT_DIR, "pffmtable"))):
    os.system("move %s %s" % (join(CURRENT_DIR, "pffmtable"), join(CURRENT_DIR, LANGUAGE_NAME + ".pffmtable")))
if (path.exists(join(CURRENT_DIR, "inttemp"))):
    os.system("move %s %s" % (join(CURRENT_DIR, "inttemp"), join(CURRENT_DIR, LANGUAGE_NAME + ".inttemp")))
if (path.exists(join(CURRENT_DIR, "normproto"))):
    os.system("move %s %s" % (join(CURRENT_DIR, "normproto"), join(CURRENT_DIR, LANGUAGE_NAME + ".normproto")))

train_cmd = join(TESSERACT_TRAINDIR, "combine_tessdata") + " " + LANGUAGE_NAME + "."
print("Executing: " + train_cmd)
os.system(train_cmd)

# If a config file is in the country's directory, use that.
config_file = join(CURRENT_DIR, country, country + '.config')
if path.isfile(config_file):
    print("Applying config file: " + config_file)
    trainedata_file = LANGUAGE_NAME + '.traineddata'
    os.system(join(TESSERACT_TRAINDIR, "combine_tessdata") + ' -o ' + trainedata_file + ' ' + config_file)

if (path.exists(join(CURRENT_DIR, LANGUAGE_NAME + ".unicharset"))):
    os.system("move %s %s" % (join(CURRENT_DIR, LANGUAGE_NAME + ".unicharset"), TEMP_DIR))
if (path.exists(join(CURRENT_DIR, LANGUAGE_NAME + ".shapetable"))):
    os.system("move %s %s" % (join(CURRENT_DIR, LANGUAGE_NAME + ".shapetable"), TEMP_DIR))
if (path.exists(join(CURRENT_DIR, LANGUAGE_NAME + ".pffmtable"))):
    os.system("move %s %s" % (join(CURRENT_DIR, LANGUAGE_NAME + ".pffmtable"), TEMP_DIR))
if (path.exists(join(CURRENT_DIR, LANGUAGE_NAME + ".inttemp"))):
    os.system("move %s %s" % (join(CURRENT_DIR, LANGUAGE_NAME + ".inttemp"), TEMP_DIR))
if (path.exists(join(CURRENT_DIR, LANGUAGE_NAME + ".normproto"))):
    os.system("move %s %s" % (join(CURRENT_DIR, LANGUAGE_NAME + ".normproto"), TEMP_DIR))
if (path.exists(join(CURRENT_DIR, LANGUAGE_NAME + ".unicharambigs"))):
    os.system("move %s %s" % (join(CURRENT_DIR, LANGUAGE_NAME + ".unicharambigs"), TEMP_DIR))