copy download_blog_posts.py .\temp\
cd temp
chcp 1255
pyinstaller download_blog_posts.py
pause
copy dist\download_blog_posts\*.* ..\dist\download_blog_posts\
cd ..
chcp 65001
