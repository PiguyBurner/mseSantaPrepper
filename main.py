import os
import zipfile
import shutil
import getopt, sys

PATH_TO_OUTPUT = "./output/"
PATH_TO_ZIPS = "./temp/zips/"
PATH_TO_TEMP_SETS = "./temp/temp_sets/"

def main():
    SATAN = False

    # Arguments to run satan-ified version
    args = sys.argv[1:]
    options = "hn"
    long_options = ["Help", "help", "Satan", "satan", "SATAN"]

    try:
        arguments, values = getopt.getopt(args, options, long_options)
        for currentArg, currentVal in arguments:
            if currentArg in ("-h", "--Help", "--help"):
                print("-n --satan: run satan version instead")
                print("-h --help: help options")
                print("\n")
                return
            elif currentArg in ("-Satan", "--satan", "--SATAN", "-n"):
                SATAN = True
    except getopt.error as err:
        print(str(err))
        return


    if SATAN:
        print("Mwahaha! Starting Satan prepper instead. Hope you prepped your Pitchfork Devils")
    else:
        print("Starting MSE Santa prepper! Hop on that Goblin Sleigh Ride.")



    # check and see if output and temp are not clear, and prompt if we clear them
    # clean up output and temp as a preemptive measure
    cleanUp(log=True, cleanOutput=True)

    #
    # SET FILES
    #
    print("Handling set files!")

    nameCounter = 0
    for file in os.listdir("./place_mse_sets_here/"):
        if file == ".gitkeep":
            continue

        print("copying file " + file)
        try:
            copyAndExtract("./place_mse_sets_here/" + file, file.replace(".mse-set", ""))
            nameCounter += 1
        except:
            print("error with extracting " + str(file) + ". Continuing on...")
    

    # For each file in temp, iterate over them
    for file in os.listdir("./temp/temp_sets"):
        if file == ".gitkeep":
            continue
        else:
            nm = file
            nm = nm.replace(".mse-set", "")

            path = "./temp/temp_sets/" + nm
            txt = getFromSetFile(path + "/set")

        # user inputted names
        print("\n\nFor the file " + file + "...")
        designer = input("Who made this gift?\n")
        reciever = input("And who is recieving this gift?\n")


        # move all the images over
        setImages = [f for f in os.listdir(PATH_TO_TEMP_SETS + file) if f.startswith("image")]
        for img in setImages:
            # copy over the images
            shutil.copy(PATH_TO_TEMP_SETS + file + "/" + img, "./temp/temp_final/" + img) # copy img over

        # move set symbol over
        setSymbology = [f for f in os.listdir(PATH_TO_TEMP_SETS + file) if f.endswith("mse-symbol")]
        for sym in setSymbology:
            shutil.copy(PATH_TO_TEMP_SETS + file + "/" + sym, "./temp/temp_final/" + sym) # copy sym over


        # Handle cards with styling already on
        txt = txt.replace("has_styling: true\n\tstyling_data:","has_styling: true\n\tstyling_data:\n\t\tremove_from_autocount: yes")

        # DFC Handling for styling 
        # put here because this is a slapjob effort that does all text together and we need the bit with other options in before we add in "remove from autocount" in below
        txt = txt.replace("other_options: ", "other_options: remove from autocount, ")

        # Handle cards that didn't have styling on
        txt = txt.replace("has_styling: false","has_styling: true\n\tstyling_data:\n\t\tremove_from_autocount: yes\n\t\tother_options: remove from autocount")


        # custom card number
        txt = txt.replace("\tcard_code_text:", "\tcustom_card_number: For " + reciever + "\n\tcard_code_text:")

        # additional credit and credit brush
        txt = txt.replace("\tcustom_card_number:", "\tadditional_credit: " + designer +"\n\tadditional_credit_brush: mechanics\n\tcustom_card_number:")


        ############## SATAN ###############
        # TODO 
        if SATAN:
            txt = txt.replace("card_code_text_3: \n", 
                              "card_code_text_3: \n" + 
                              "\tvorthos_box: SATAN\n")


        # illustrator overwrites
        # TODO maybe find more of these 
        ###
        txt = txt.replace(": Art by Santa\n", ": " + designer + "\n")
        txt = txt.replace(": Santa\n", ": " + designer  + "\n")
        txt = txt.replace(": Me\n", ": " + designer + "\n")

        # Satan replacements
        txt = txt.replace(": Art by Satan\n", ": " + designer + "\n")
        txt = txt.replace(": Satan\n", ": " + designer  + "\n")
        # TODO alert how many of these were changed?

        # actually save the text into a set file
        f = open("./temp/temp_final/set", "w", encoding="utf-8")
        f.write(txt)
        f.close()
        
        # save off in temp_final
        zf = zipfile.ZipFile("./output/" + file + ".mse-set", mode="w")
        try:
            for filename in os.listdir("./temp/temp_final/"):
                if filename == ".gitkeep" and filename == file + ".mse-set":
                    continue
                zf.write("./temp/temp_final/" + filename, filename, compress_type=zipfile.ZIP_DEFLATED)
        except FileNotFoundError:
            print("that's really odd; file not found despite checking for all the files here")
        finally:
            zf.close()
            

        #############################
        # COMMENT THIS OUT TO DEBUG # 
        #############################
        # clean up temp_final for the next guy
        emptyDir("./temp/temp_final/")


        print("Done with " + file)

    #############################
    # COMMENT THIS OUT TO DEBUG # 
    #############################
    cleanUp()


    print("Done! Hope you got your Just Desserts :p")
    print("Please go double-check the files!!!")

def cleanUp(log=False, cleanOutput=False):
    if len(os.listdir("./temp/temp_sets/")) > 1:
        if log:
            print("temp_sets folder has junk in there. Cleaning it up...")
        emptyDir("./temp/temp_sets/")

    if len(os.listdir("./temp/zips/")) > 1:
        if log:
            print("zips folder has junk in there. Cleaning it up...")
        emptyDir("./temp/zips/")

    if len(os.listdir("./temp/temp_final/")) > 1:
        if log:
            print("temp final folder has junk in there. Cleaning it up...")
        emptyDir("./temp/temp_final/")

    if len(os.listdir("./output/")) > 1 and cleanOutput:
        if log:
            print("Output folder has the following files:")
            for file in os.listdir("./output/"):
                if file != ".gitkeep":
                    print(file)
            if input("\nDelete these files? Y for yes, n for no.\n") != "Y":
                raise KeyboardInterrupt("Go get everything you need out of output!") 
        else:
            emptyDir("./output/")



def copyAndExtract(filepath, newFilename):
    temp_path = PATH_TO_TEMP_SETS

    shutil.copy(filepath, PATH_TO_ZIPS + newFilename + ".zip")

    with zipfile.ZipFile(PATH_TO_ZIPS + newFilename + ".zip", 'r') as zip_ref:
        zip_ref.extractall(temp_path + newFilename)
 
# this script always overwrites rather than appending
def appendToOutputSetFile(arr, overwrite=False):
    if overwrite:
        f = open("./output/set", "w", encoding="utf-8")    
    else:
        f = open("./output/set", "a", encoding="utf-8")    

    for i in arr:
        f.write(i)
    
    f.close()

# pulls text from the set file based on the start and end indicators (end indicator is not included)
# this script just pulls all of it always
def getFromSetFile(filepath, startIndicator="", endIndicator="", stopper=False):
    f = open(filepath, "r", encoding="utf-8")
    txt = f.read()
    f.close()

    startOfBlock = 0
    if startIndicator != "":
        startOfBlock = -1
        for i in range(len(txt)):
            if startIndicator == txt[i]:
                startOfBlock = i
                break

    endOfBlock = len(txt)
    if endIndicator != "":
        endOfBlock = -1
        for j in range(len(txt)):
            if endIndicator in txt[j]:
                endOfBlock = j
                break
    
    # could be from older versions; they didn't use underscores in "version_control" tag
    if startOfBlock == -1 or endOfBlock == -1:
        print("not found start nor end of card block... weird.")
        print("Try opening the set file anyways when done; it might work still if I'm good at debugging.")
        if not stopper:
            startIndicator = startIndicator.replace("_", " ")
            endIndicator = endIndicator.replace("_", " ")
            return getFromSetFile(filepath, startIndicator, endIndicator, stopper=True)


    return txt[startOfBlock:endOfBlock]

def emptyDir(path):
    contents = os.listdir(path)

    for obj in contents:
        if obj == ".gitkeep":
            continue

        if os.path.isdir(path + obj):
            emptyDir(path + obj + "/")
            os.rmdir(path + obj) 
        else:
            os.remove(path + obj)

if __name__ == "__main__":
    main()