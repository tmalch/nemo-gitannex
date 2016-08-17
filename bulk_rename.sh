#!/bin/bash

#This script is thought to be used as very simple bulk renamer for nemo 
#  go to Edit->Preferences->Behavior
#  under "Command to invoke when renaming multiple items:" enter "bulk_rename.sh %F" 
#
#What it does: 
# takes a list of filenames as input, 
# asks the user for a new name
# and renames all given files to the schema <new name>(<counter>)[.<original ending>] 


dry=0 #if set to 1 no rename operations are executed but all commands are shown as text
dryres=""
err_src_does_not_exist=""
err_dst_already_exist=""
err_could_not_move=""

version=$(nemo --version|tr -dc [:digit:])
if [ "$version" -lt "287" ]; then
    zenity --error --text "Sorry your version of Nemo has a bug (https://github.com/linuxmint/nemo/issues/614)\nTherefore this script cannot work. You have to use Nemo >= 2.8.7" &
    exit 0
fi

bname=$(zenity --entry --title="enter new base name")
if [ $? -ne 0 ]; then
    exit 0
fi

i=0
for arg in "$@"
do
    # nemo escapes blanks in filenames with %20
    # https://gist.github.com/cdown/1163649
    arg="${arg//+/ }"
    fileurl="$( printf '%b' "${arg//%/\\x}" )"
    name="${fileurl#file://*}"
    dirname=$(dirname "$name")
    if [ -d "$name" ]; then
        ending=""
    elif [ -f "$name" -o -L "$name" ]; then
        ending=".${name##*.}"
        if [ "$ending" = ".$name" ]; then
            ending=""
        fi
    else
        err_src_does_not_exist="${err_src_does_not_exist}$name\n"
        continue
    fi
    i=$((i+1))
    newname="$dirname/$bname($i)$ending"
    if [ -e "$newname" -o -L "$newname" ]; then
        err_dst_already_exist= "${err_dst_already_exist}could not rename $name to $newname\n"
        continue
    fi
    if [ $dry -eq 1 ]; then
        dryres=$dryres"mv -n -T "$name" "$newname"\n"
    else
        mv -n -T "$name" "$newname" || err_could_not_move="${err_could_not_move}$name to $newname\n"
    fi
done

err_msg=""
if [ -n "$err_src_does_not_exist" ]; then
    err_msg="${err_msg}Source does not exist:\n"
    err_msg="$err_msg $err_src_does_not_exist"
fi
if [ -n "$err_dst_already_exist" ]; then
    err_msg="${err_msg}File already exists:\n"
    err_msg="$err_msg $err_dst_already_exist"
fi
if [ -n "$err_could_not_move" ]; then
    err_msg="${err_msg}Could not rename:\n"
    err_msg="$err_msg $err_could_not_move"
fi
if [ -n "$err_msg" ]; then
    zenity --error --text "$err_msg"
fi

if [ $dry -eq 1 ]; then
    zenity --info --text "$dryres"
fi








