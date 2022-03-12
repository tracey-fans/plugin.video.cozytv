# Zip up the code to distribute to Kodi. Don't use Github's download zips, they
# don't work at all!!

# First remove any remaining data
rm -f Cozytv.zip

# Copy the license file
cp ../LICENSE ./plugin.video.cozytv/LICENSE.md

# Rename the screenshot files -- their names clash in the "DOS 8.3" zipping
mv ./plugin.video.cozytv/resources/media/screenshot-01.jpg ./plugin.video.cozytv/resources/media/01ss.jpg 
mv ./plugin.video.cozytv/resources/media/screenshot-02.jpg ./plugin.video.cozytv/resources/media/02ss.jpg 
mv ./plugin.video.cozytv/resources/media/screenshot-03.jpg ./plugin.video.cozytv/resources/media/03ss.jpg 

# Do the zipping. In Windows, the following command will probably be okay:
#
#     zip -rq ./Cozytv.zip ./plugin.video.cozytv
#
#  (and all the following stuff with "7z rn" can be omitted). On Linux we need to
#  use the -k option.
#

zip -rqk ./Cozytv.zip ./plugin.video.cozytv

# Done with the license file and screenshots
rm -f ./plugin.video.cozytv/LICENSE.md
mv ./plugin.video.cozytv/resources/media/01ss.jpg ./plugin.video.cozytv/resources/media/screenshot-01.jpg 
mv ./plugin.video.cozytv/resources/media/02ss.jpg ./plugin.video.cozytv/resources/media/screenshot-02.jpg 
mv ./plugin.video.cozytv/resources/media/03ss.jpg ./plugin.video.cozytv/resources/media/screenshot-03.jpg 

# Now this is a hack to get zip working in Linux. See:
#
#   https://superuser.com/questions/898481/how-to-create-a-zip-file-with-files-in-fat-format-on-linux
#
# We need to zip with the "-k" option to get FAT files, but then must rename each
# one individually using the "7z rn" option to restore normal filenames (not
# the 8.3 ones).

7z rn Cozytv.zip PLUGIN.VID plugin.video.cozytv  1> /dev/null

7z rn Cozytv.zip plugin.video.cozytv/LICENSE.MD plugin.video.cozytv/LICENSE.md  1> /dev/null
7z rn Cozytv.zip plugin.video.cozytv/MAIN.PY plugin.video.cozytv/main.py  1> /dev/null
7z rn Cozytv.zip plugin.video.cozytv/ADDON.XML plugin.video.cozytv/addon.xml  1> /dev/null

7z rn Cozytv.zip plugin.video.cozytv/RESOURCE plugin.video.cozytv/resources  1> /dev/null

7z rn Cozytv.zip plugin.video.cozytv/resources/SETTINGS.XML plugin.video.cozytv/resources/settings.xml  1> /dev/null
7z rn Cozytv.zip plugin.video.cozytv/resources/__INIT__.PY plugin.video.cozytv/resources/__init__.py  1> /dev/null

7z rn Cozytv.zip plugin.video.cozytv/resources/MEDIA plugin.video.cozytv/resources/media  1> /dev/null
7z rn Cozytv.zip plugin.video.cozytv/resources/LIB plugin.video.cozytv/resources/lib  1> /dev/null
7z rn Cozytv.zip plugin.video.cozytv/resources/LANGUAGE plugin.video.cozytv/resources/language  1> /dev/null

7z rn Cozytv.zip plugin.video.cozytv/resources/media/01SS.JPG plugin.video.cozytv/resources/media/screenshot-01.jpg  1> /dev/null
7z rn Cozytv.zip plugin.video.cozytv/resources/media/02SS.JPG plugin.video.cozytv/resources/media/screenshot-02.jpg  1> /dev/null
7z rn Cozytv.zip plugin.video.cozytv/resources/media/03SS.JPG plugin.video.cozytv/resources/media/screenshot-03.jpg  1> /dev/null
7z rn Cozytv.zip plugin.video.cozytv/resources/media/FANART.JPG plugin.video.cozytv/resources/media/fanart.jpg  1> /dev/null
7z rn Cozytv.zip plugin.video.cozytv/resources/media/ICON.PNG plugin.video.cozytv/resources/media/icon.png  1> /dev/null

7z rn Cozytv.zip plugin.video.cozytv/resources/lib/RUN_ADDO.PY plugin.video.cozytv/resources/lib/run_addon.py  1> /dev/null
7z rn Cozytv.zip plugin.video.cozytv/resources/lib/__INIT__.PY plugin.video.cozytv/resources/lib/__init__.py  1> /dev/null

7z rn Cozytv.zip plugin.video.cozytv/resources/language/RESOURCE.LAN plugin.video.cozytv/resources/language/resource.language.en_gb  1> /dev/null
7z rn Cozytv.zip plugin.video.cozytv/resources/language/resource.language.en_gb/STRINGS.PO plugin.video.cozytv/resources/language/resource.language.en_gb/strings.po  1> /dev/null

# The zip is ready! Rename it manually and copy to ../zips/ directory.
