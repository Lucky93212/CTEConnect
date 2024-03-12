# CTEConnect
![long_logo](https://github.com/Lucky93212/CTEConnect/assets/63886761/b1b10760-6c1b-4df6-9807-b90abd4cc3d7)
CTEConnect is the next premier online employment and opportunity platform geared towards usage by high school students, parents, teachers, and administrators.

## Features
* <b>Comprehensive opportunities library:</b> CTEConnect offers a comprehensive library of internships, programs, research fellowships, and other venues of employment from across numerous employers.
* <b>Application lifecycle management:</b> Completely manages the lifecycle of applying to programs and integrates with third party application systems.
* <b>Detailed Reporting:</b> Students, Parents, and all necessary faculty members will have the ability to instantly see reports regarding student mentorship hours and involvement.
* <b>Administrator Oversight:</b> Student progress can be monitored at numerous levels which allows everyone to understand how students interact with employers and ensure that students are truly career ready.

## Development
* <a href="https://www.djangoproject.com/">Django</a> -- Primary framework for the website which allows for web page rendering as well as all backend technology. Django comes with a full suite of features that ensures security including CSRF tokens, host header validation, and cross site scripting (XSS) protection.
* <a href="https://www.sqlite.org/">SQLite3</a> -- SQLite3 is utilized in order to store user information as well as other models including businesses, hours requests, WBL Opportunities, etc. SQLite3 is preferable as it integrates easily with Django.
* Added benefit of utilizing a SQLite3 database as opposed to the tradition MySQL database is that SQLite3 can be stored locally. In addition, through the <a href="https://www.microsoft.com/en-us/microsoft-365/onedrive/online-cloud-storage">OneDrive</a> integration, the SQLite3 database is constantly backed up to the cloud.
* No costs associated with it due to the benefits provided by the GitHub Student Developer Pack. OneDrive provides constant database backup so a new database can be created in an integrity breach.
The website is also written in a manner such that it firsts refers to a requests “url pattern” and then the corresponding function handles the request allowing for a selection form of running the program.

## Installation

* Clone the repo via the command `git clone https://github.com/Lucky93212/CTEConnect`
* Open a terminal in the cloned folder.
* Ensure you have the relevant dependancies installed including Python, Django, and the necessary Python libraries, if not be sure to install them via the `pip install [LIBRARY]` command.
* Run the command `py manage.py runserver`
* The client should be running on `http://127.0.0.1:8000`

<br>
<div align="center">
© Copyright 2024 <a href="https://github.com/Lucky93212">@Lucky93212</a>. All Rights Reserved.

Unauthorized copying or redistribution of this work is strictly prohibited.

Made in America.
</div>
