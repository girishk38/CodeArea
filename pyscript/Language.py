# Author    :   Girish Kumar
# Date      :   15-april-2018
# Info      :   Language information

# FORMAT =   "LANGUAGE"                "Extension"      "COMMAND 1"
#               "BINARY"                "COMMAND 2"
LANGUAGE = {0: {"title": "python 2.6", "extension": "py",  "command1": "python2 {}/CodeArea.py"},
            1: {"title": "python 3.5", "extension": "py",  "command1": "python3 {}/CodeArea.py"},
            #############################
            # two step languages
            #############################
            2: {"title": "golang",     "extension": "go",  "command1": "go build -o {0}/CodeArea.out {0}/CodeArea.go",
                "binary": "CodeArea.out", "command2": "{}/CodeArea.out"},
            3: {"title": "C",          "extension": "c",   "command1": "gcc -O3 {0}/CodeArea.c -o {0}/CodeArea.out",
                "binary": "CodeArea.out", "command2": "{}/CodeArea.out"},
            4: {"title": "Cpp",        "extension": "cpp", "command1": "g++ -O3 {0}/CodeArea.cpp -o {0}/CodeArea.out",
                "binary": "CodeArea.out", "command2": "{}/CodeArea.out"},
            5: {"title": "java",       "extension": "java", "command1": "javac {0}/CodeArea.java",
                "binary": "CodeArea.class", "command2": "java -cp /{}/ CodeArea"}
            }


TWO_STEP = 1


# language      id
# python 2      0
# python 3      1
# golang        2
# C             3
# Cpp           4
# java          5