# GibranGodoy

## Project 3

**Web Programming with Python and JavaScript**
## Pizza App
For this project it was needed to build a web application for handling a pizza restaurant's online orders. The objective was to able the users to browse the restaurant's menu, add items to their cart and submit their orders. Meanwhile, the restaurant owners (*admin*) was able to add and update menu items. Also, the admin has the oportunity to view orders that have been placed.

#### The main files are:
- `admin.py`
- `models.py`
- `urls.py`
- `views.py`

On `models.py` there are the models or the tables created for the app. Here is specified all the chacarteristics of each category. The data was obtained from [Pinnochio’s Pizza & Subs](http://www.pinocchiospizza.net/menu.html).

On the file `admin.py` are  the correspondig functions to able to see the information on the admin page of the app.

The `urls.py` are declarated the paths to each fuction on the `view.py` file.

`view.py` is the analog to `application.py` from FLASK. The app is controlled by this code and here are called the html files.

#### Personal touch
The administrator has the possibility to mark orders as complete and allowing users to see the status of their pending or completed orders.