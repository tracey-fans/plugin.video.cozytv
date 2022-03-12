# A Python 3 script for building the zip files to distribute this plugin.
#


import sys
import subprocess
import pathlib
import shutil



__plugin_name__ = "plugin.video.cozytv"




def build():
  
    _ZIP_NAME = "Cozytv.zip"
    _ROOT_NAME = __plugin_name__
    _BUILD_DIR = "_build"



    def make_dos8_3_filename(fn_in):
        c = fn_in.split(".")
        if len(c) == 1:
            return c[0][:8].upper()
        else:
            return c[0][:8].upper() + "." + c[1][:3].upper()





    def build_windows():
        # Build on windows

        # Note: this is untested!

        subprocess.run(["zip", "-rq", f"../{_ZIP_NAME}", f"./{_ROOT_NAME}"], cwd=_BUILD_DIR)
        return
        
        
        
    def build_linux():
        # Build on linux
        
        # Here, we need to use the -k option


        i = 1
        
        renames  = []

        for pp in pathlib.Path(_BUILD_DIR, _ROOT_NAME, "resources", "media").iterdir():
            if len(pp.stem) > 8:
                # Won't fit in the 8.3 naming scheme
                
                new_name = "{0:06d}".format(i) + pp.suffix.upper()
                
                renames.append(   (pp.name, new_name)   )
                
                pp.rename(pp.parent.joinpath(new_name))
                
                i += 1
                




        subprocess.run(["zip", "-rqk", f"../{_ZIP_NAME}", f"./{_ROOT_NAME}"], cwd=_BUILD_DIR)
        

        # Now this is a hack to get zip working in Linux. See:
        #
        #   https://superuser.com/questions/898481/how-to-create-a-zip-file-with-files-in-fat-format-on-linux
        #
        # We need to zip with the "-k" option to get FAT files, but then must rename each
        # one individually using the "7z rn" option to restore normal filenames (not
        # the 8.3 ones).


        with open("/dev/null", "w") as _NULL_DEV:

            subprocess.run(["7z", "rn", _ZIP_NAME, make_dos8_3_filename(_ROOT_NAME), _ROOT_NAME], stdout=_NULL_DEV)

            subprocess.run(["7z", "rn", _ZIP_NAME, f"{_ROOT_NAME}/LICENSE.MD", f"{_ROOT_NAME}/LICENSE.md"], stdout=_NULL_DEV)
            subprocess.run(["7z", "rn", _ZIP_NAME, f"{_ROOT_NAME}/MAIN.PY", f"{_ROOT_NAME}/main.py"], stdout=_NULL_DEV)
            subprocess.run(["7z", "rn", _ZIP_NAME, f"{_ROOT_NAME}/ADDON.XML", f"{_ROOT_NAME}/addon.xml"], stdout=_NULL_DEV)

            subprocess.run(["7z", "rn", _ZIP_NAME, f"{_ROOT_NAME}/RESOURCE", f"{_ROOT_NAME}/resources"], stdout=_NULL_DEV)

            subprocess.run(["7z", "rn", _ZIP_NAME, f"{_ROOT_NAME}/resources/SETTINGS.XML", f"{_ROOT_NAME}/resources/settings.xml"], stdout=_NULL_DEV)
            subprocess.run(["7z", "rn", _ZIP_NAME, f"{_ROOT_NAME}/resources/__INIT__.PY", f"{_ROOT_NAME}/resources/__init__.py"], stdout=_NULL_DEV)

            subprocess.run(["7z", "rn", _ZIP_NAME, f"{_ROOT_NAME}/resources/MEDIA", f"{_ROOT_NAME}/resources/media"], stdout=_NULL_DEV)
            subprocess.run(["7z", "rn", _ZIP_NAME, f"{_ROOT_NAME}/resources/LIB", f"{_ROOT_NAME}/resources/lib"], stdout=_NULL_DEV)
            subprocess.run(["7z", "rn", _ZIP_NAME, f"{_ROOT_NAME}/resources/LANGUAGE", f"{_ROOT_NAME}/resources/language"], stdout=_NULL_DEV)

            subprocess.run(["7z", "rn", _ZIP_NAME, f"{_ROOT_NAME}/resources/media/FANART.JPG", f"{_ROOT_NAME}/resources/media/fanart.jpg"], stdout=_NULL_DEV)
            subprocess.run(["7z", "rn", _ZIP_NAME, f"{_ROOT_NAME}/resources/media/ICON.PNG", f"{_ROOT_NAME}/resources/media/icon.png"], stdout=_NULL_DEV)
            for qq in renames:
                subprocess.run(["7z", "rn", _ZIP_NAME, "plugin.video.cozytv/resources/media/" + qq[1], f"{_ROOT_NAME}/resources/media/" + qq[0]], stdout=_NULL_DEV)


            subprocess.run(["7z", "rn", _ZIP_NAME, "plugin.video.cozytv/resources/lib/RUN_ADDO.PY", f"{_ROOT_NAME}/resources/lib/run_addon.py"], stdout=_NULL_DEV)
            subprocess.run(["7z", "rn", _ZIP_NAME, "plugin.video.cozytv/resources/lib/__INIT__.PY", f"{_ROOT_NAME}/resources/lib/__init__.py"], stdout=_NULL_DEV)

            subprocess.run(["7z", "rn", _ZIP_NAME, f"{_ROOT_NAME}/resources/language/RESOURCE.LAN", f"{_ROOT_NAME}/resources/language/resource.language.en_gb"], stdout=_NULL_DEV)
            subprocess.run(["7z", "rn", _ZIP_NAME, f"{_ROOT_NAME}/resources/language/resource.language.en_gb/STRINGS.PO", f"{_ROOT_NAME}/resources/language/resource.language.en_gb/strings.po"], stdout=_NULL_DEV)





    # Remove the build directory and all its contents
    try:
        shutil.rmtree(_BUILD_DIR)
    except FileNotFoundError:
        pass
      
    # Remove the output
    try:
        pathlib.Path(_ZIP_NAME).unlink()
    except FileNotFoundError:
        pass
    


    # Make the empty directory
    pathlib.Path(_BUILD_DIR).mkdir()

    # Copy in the source
    shutil.copytree(_ROOT_NAME, pathlib.Path(_BUILD_DIR).joinpath(_ROOT_NAME))

    # Copy in the license file
    shutil.copyfile(pathlib.Path("..").joinpath("LICENSE"), pathlib.Path(_BUILD_DIR).joinpath(_ROOT_NAME, "LICENSE.md"))



    if sys.platform.startswith("linux"):
        build_linux()
    else:
        build_windows()


build()
