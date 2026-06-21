# MSE Santa Prepper
This python script preps all Santa files for the final Egghub upload

## How to Use
0. install python if you don't have it already. Just google it.

1. Put all the mse-set files into the folder "place_mse_sets_here"

3. Open up your terminal and go to this location (`cd <wherever it's stored>/mseSantaPrepper`)

4. type `python main.py` in the command line and run it

5. There are a few printouts; please listen to them!

6. Try opening each set file in MSE!
**NOTE: Whenever you run the script, it will clear out the output file! Listen to the printouts!

## Additional Notes

If you are getting some things complaining, make sure you have the most recent MSE. 

If things still complain, try opening up and re-saving the files. This was built with newer versions (as of 5/27/26) in mind; hopefully not much has changed and my error handling is adequate enough

I doubt this code is perfect but it succeeded in my testing so that's good enough for me. Hopefully it helps whoever needs it, and don't judge my code

If you are trying to debug it manually, comment out "cleanup()" on line 107 to keep all the unpacked files around.