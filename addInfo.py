import csv
import sys
import argparse
import time


def readFile(file):
    try:
        open(file)
    except IOError:
        print "Error: cannot open %s. Please submit a valid file" % (file)
        sys.exit()
    colList = []
    mainList = []
    if ".csv" in file:
        print "Comma chosen as delimiter"
        delStr = ','
    else:
        print "Tab chosen as delimiter"
        delStr = '\t'
    with open(file) as r:
        reader = csv.reader(r, delimiter=delStr)
        for row in reader:
            for col in row:
                colList.append(col)
            mainList.append(colList[0:])
            colList[:] = []
    print "%s lines read in from %s" % (str(len(mainList)), file)
    return mainList

def addColumn(list1, list2, c1, c2, i, h, out_file):
    colList = []
    outList = []
    chunkSize = 100
    # This just checks the length of the list being appended, and allows chunks to be written
    if len(list1) > chunkSize:
        longList = True
        print "Chunk size of %s exceeded. File will be processed in chunks of %s lines" % (str(chunkSize), str(chunkSize))
    else:
        longList = False

    hasName = False
    name = ""

    # This appends the header to the new list 'outList', if '-H' flag is selected
    if len(h) > 1:
        start = 1
        for x in range(0, len(list1[0])):
            colList.append(list1[0][x])
        colList.append(h)
        outList.append(colList[0:])
    else:
        start = 0

    # Main comparison bit here
    position = 0
    checkpoint = 0
    for x in range(start, len(list1)):
        colList[:] = []
        compare = str(list1[x][c1])
        for y in range(0, len(list2)):
            if compare in str(list2[y][c2]):
                # hasName = True
                name = str(list2[y][i])
                break
        for z in range(0, len(list1[x])):
            colList.append(list1[x][z])
        colList.append(name)
        outList.append(colList[0:])
        name = ""
        position += 1

        # If 'list1' contains more than 'chunkSize' lines, then this allows the output file to be made
        # and appended in 'chunkSize'-piece chunks
        if position >= chunkSize:
            if checkpoint < position:
                writeOutput(outList, out_file, True)
                print "Creating file %s" % (out_file)
            else:
                writeOutput(outList, out_file, False)
            checkpoint += position
            position = 0
            print "%s/%s lines updated" % (str(checkpoint), str(len(list1)))
            outList[:] = []

    if not longList:
        writeOutput(outList, out_file, True)
        print "%s lines left after processing" % (str(len(outList)))
    else:
        writeOutput(outList, out_file, False)
    # return outList
    # Need to make a recursive script to continually write outputs

def rearrangeProteins(list, fileName):
    # This function is used to ensure all amino acid sequences only span one line
    outList = []
    out_str = ""
    for x in range(0, len(list)):
        if '>' in str(list[x]):
            if len(out_str) > 0:
                outList.append(out_str)
            out_str = ""
            outList.append(str(list[x][0]))
        elif len(str(list[x])) > 0:
            out_str += str(list[x][0])
    outList.append(out_str)
    outList2 = []
    colList = []
    for x in range(0, len(outList), 2):
        colList.append(outList[x])
        colList.append(outList[x+1])
        outList2.append(colList[0:])
        colList[:] = []
    print "%s lines left after rearranging %s" % (str(len(outList2)), fileName)
    return outList2

def writeOutput(output, out_file, overwrite):
    if overwrite:
        with open(out_file, 'wb') as w:
            writer = csv.writer(w)
            writer.writerows(output)
            #print "Output written to %s" % out_file
    else:
        with open(out_file, 'a') as w:
            writer = csv.writer(w)
            writer.writerows(output)


# Begin main script here
parser = argparse.ArgumentParser()
parser.add_argument('File1', help="File to be added to, csv or tab-delimited format")
parser.add_argument('File2', help="File with info to be taken from, in csv or tab-delimited format")
parser.add_argument('-1', '--column1', help="Set column number in File1 to be compared. Default is 1")
parser.add_argument('-2', '--column2', help="Set column number in File2 to be compared. Default is 1")
parser.add_argument('-i', '--info_column', help="Select which column in File2 to add to File1. Default is 2")
parser.add_argument('-H', '--header', help="Does File1 have a header line?")
parser.add_argument('-f', '--fasta', help="Sets expected format for File2 to be .fasta format", action="store_true")
parser.add_argument('-o', '--output', help="Set name of output file")

# Error catch 1: Make sure that some arguments have been supplied
try:
    args = parser.parse_args()
except SystemExit:
    print "Please enter valid file type \ntype 'python addInfo.py -h for help'"
    sys.exit()

args = parser.parse_args()
starttime = time.time()

# Make sure everything is behaving as expected
if args.output:
    out_file = args.output
else:
    out_file = "%s_info.csv" % (args.File1[:-4])

if args.column1:
    c1 = int(args.column1) - 1
else:
    c1 = 0

if args.column2:
    c2 = int(args.column2) - 1
else:
    c2 = 0

if args.info_column:
    i = int(args.info_column) - 1
else:
    i = 1

if args.header:
    header = str(args.header)
else:
    header = ""

# Now, start proper program here
list1 = readFile(args.File1)
list2 = readFile(args.File2)
if args.fasta:
    list2 = rearrangeProteins(list2, args.File2)
    addColumn(list1, list2, c1, 0, 0, header, out_file)
else:
    addColumn(list1, list2, c1, c2, i, header, out_file)

print "Process took %s seconds" % (str(time.time() - starttime))