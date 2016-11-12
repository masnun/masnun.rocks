import subprocess 
import os
import re
import sys
import shutil

if len(sys.argv) > 1:
        SOURCE = sys.argv[1]
else:
        print("Please pass your hugo output directory. It is generally named `public`")
        sys.exit()


TMP = ".hugo_tmp_clean"

## Generate the files in a temp location
p = subprocess.Popen(
        "hugo -d {}".format(TMP), 
        shell=True, 
        stdout=subprocess.PIPE

        )

p.communicate()

## Recursively iterare through a directory and create a set of unique files / sub dirs
## Source - StackOverflow

def build_files_set(rootdir):
    root_to_subtract = re.compile(r'^.*?' + rootdir + r'[\\/]{0,1}')

    files_set = set()
    for (dirpath, dirnames, filenames) in os.walk(rootdir):
        for filename in filenames + dirnames:
            full_path = os.path.join(dirpath, filename)
            relative_path = root_to_subtract.sub('', full_path, count=1)
            files_set.add(relative_path)

    return files_set

## Grab the files and sub directories 
## Get diff of the sets 
## Source - StackOverflow

def compare_directories(dir1, dir2):
    files_set1 = build_files_set(dir1)
    files_set2 = build_files_set(dir2)
    return (files_set1 - files_set2, files_set2 - files_set1)


## Compare the files 
src, tmp = compare_directories(SOURCE, TMP) 

print("Files that can be deleted in {}:".format(SOURCE))

for x in src:
        if ".git" in x or x in sys.argv[1:]:
                continue
        
        print(x)

        
shutil.rmtree(TMP)
