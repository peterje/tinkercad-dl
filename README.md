# tinkercad-dl

A tool to autonomously download TinkerCAD files.

Given a list of unique user IDs, a name of a design, and login info, this tool will visit the page of each student and look for a design with the provided title. It will then convert the model to a .schematic.

# Requirements

- Python 3 (https://www.python.org/downloads/)
- Selenium (https://pypi.org/project/selenium/)
- Firefox Version >= 60 (https://www.mozilla.org/en-US/firefox/new/)

# Example Usage

python3 tinker.py --namesfile="my_students.txt" --design="House" --username="TeacherAccount" --password="abc123"

Will visit look for a design titled "House" for each account listed in "my_students.txt". When found it will open up the page for changes or export.
