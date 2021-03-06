#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''Convert csv file to lua script'''

import os
import os.path
import csv
import gl

def get_outputfile_name(inputname):
    # if inputEnds not in inputname:
    #     print("error file: ", inputname)
    #     return
    outputDirName = os.path.join(os.getcwd(), gl.outputDir)
    return outputDirName + inputname + gl.outputEnds
    # return os.path.join(outputDirName, outputname)

def write2lua(filekey, f, row, i, keysArr, typesArr):
    try:
        newDefine = False
        if row[0] != "":
            if typesArr[0].lower() == gl.typeInt:
                gl.name = "str" + row[0]
            else:
                gl.name = row[0]
            gl.level = 1
            newDefine = True
        if newDefine:
            f.writelines(filekey + "." + gl.name + " = {\n")
            for index, item in enumerate(row):
                if index >= 1:
                    k = keysArr[index]
                    t = typesArr[index].lower()
                    if t == gl.typeInt:
                        if item == "":
                            f.writelines("    " + k + " = " + "0,\n")
                        else:
                            f.writelines("    " + k + " = " + item + ",\n")
                    elif t == gl.typeBool:
                        if item == "":
                            f.writelines("    " + k + " = " + "false,\n")
                        else:
                            f.writelines("    " + k + " = " + item.lower() + ",\n")
                    elif t == gl.typeStr:
                        f.writelines("    " + k + ' = "' + item + '",\n' )
                    else:
                        print ('Error, unsupport type: ', t, filekey)
                        return
            f.writelines("}\n\n")

        f.writelines(filekey + "." + gl.name + "[" + str(gl.level) + "] = {\n")
        for index, item in enumerate(row):
            if item == "":
                continue
            if index >= 1:
                k = keysArr[index]
                t = typesArr[index].lower()
                if t == gl.typeInt:
                    f.writelines("    " + k + " = " + item + ",\n")
                elif t == gl.typeBool:
                    f.writelines("    " + k + " = " + item.lower() + ",\n")
                elif t == gl.typeStr:
                    f.writelines("    " + k + ' = "' + item + '",\n' )
                else:
                    print ('Error, unsuppurt type: ', t, filekey)
                    return

        f.writelines("}\n\n")
        gl.level += 1
    except Exception:
        print (Exception)

def convert2lua(inputname):
    try:
        with open(inputname, newline = '') as f:
            reader = csv.reader(f)

            print ("write start")
            tempkey = inputname[:-4]
            # outputname = get_outputfile_name(tempkey)
            filekey = str.split(tempkey, "/")[-1]
            outputname = get_outputfile_name(filekey)
            print("!!!: ", outputname, filekey)
            f = open(outputname, "w")
            f.write("-- this file is generated by program!\n-- never modify it!!!\n-- source file: " + filekey + ".csv\n\n")
            f.writelines("local " + filekey + " = {}\n\n")

            i = 0
            allType = []
            for row in reader:
                i += 1
                if len(row) <= 0:
                    print ('Error, len(row) <= 0', inputname, i)
                    return
                if i == gl.keyLine:
                    gl.keysArr = row
                    continue
                if i == gl.typeLine:
                    gl.typesArr = row
                    continue
                if i >= gl.defineLine:
                    if len(gl.keysArr) <= 0 or len(gl.typesArr) <= 0:
                        print ('Error, no keysArr or typesArr', i, gl.keysArr, gl.typesArr)
                        return
                    # 兼容第一列是int的情况 未处理第一列是bool的情况
                    # 业务保证第一列是sting或者int 最好是string
                    if row[0] != "":
                        if gl.typesArr[0] == gl.typeInt:
                            allType.append("str" + row[0])
                        else:
                            allType.append(row[0])
                write2lua(filekey, f, row, i, gl.keysArr, gl.typesArr)

            f.writelines(filekey + ".all_type = {}\n")
            f.writelines("local all_type = " + filekey + ".all_type\n")
            for index, item in enumerate(allType):
                f.writelines("all_type[" + str(index+1) + "] = " + item + "\n")
            f.writelines("\nfor i = 1, #(" + filekey + ".all_type) do\n")
            f.writelines("    local item = " + filekey + ".all_type[i]\n")
            f.writelines("    for j = 1, #item do\n")
            f.writelines("        item[j].__index = item[j]\n")
            f.writelines("        if j < #item then\n")
            f.writelines("            setmetatable(item[j+1], item[j])\n")
            f.writelines("        end\n")
            f.writelines("    end\n")
            f.writelines("end\n\n\n")
            f.writelines("return " + filekey)

            f.close()
    except Exception:
        print (Exception)
        print ('Error, fail convert:', inputname)
        print ()

def get_filename_list(dirname):
    flist = []
    for root, dirs, files in os.walk(dirname):
        for name in files:
            if name.endswith(gl.inputEnds):
                flist.append(os.path.join(root, name))
    return flist

def explore():
    inputDirName = os.path.join(os.getcwd(), gl.inputDir)
    flist = get_filename_list(inputDirName)
    for fname in flist:
        print(fname)
        convert2lua(fname)
    print("Finished!")

if __name__ == '__main__':
    explore()
