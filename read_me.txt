Steps To run the app:

1. Place the api in localhost
2. Include the database spritle.sql
3. Make sure this folder has file permission to read and write files
4. install python 2.7 with modules requests,tkinter
5. Make sure the app runs first time with the local host on so that it will fetch the data and store it in local in file post.json
6. For each operation it will check for internet connection  and update the content.
7. If the internet is not found it will store the values in local system under file name offline_post.json
8. When the app runs next time with internet connection it will update automatically(Tried automatically checking for internet evey 10secs because of many error stopped that code is still there under commented portion)
9. For delete type will be included
10. If the post has id then it will update the row . Else it will insert row.
12. Frame will update after every command.