# Warships
Online battleships game on Django framework

# Prerequisites
```
python3
django 3.0.4
psycopg2
postgresql
pytest-django 3.8.0
```

# Installation
```
Optional: Create virtual environment.
1. Create project and app in django framework.
2. Set up database connection in settings.py (postgresql because of the way how arrays are stored in DB).
3. Replace and add files included in this repository.
4. Run server.
```

# Running tests
```
Preferably in virtual environment.
1. In terminal use: export DJANGO_SETTINGS_MODULE=[name of project].settings
2. Run: pytest-3 <path to your tests.py>
```

# How does it work and look like?
```
After login you have access to dashboard where you can challenge another players:
```

<img src="https://imgur.com/bcXopVR.png" />
<img src="https://imgur.com/PKM9QaZ.png" />

```
Then, challenged user has two options. Either to accept or reject challenge.
```

<img src="https://imgur.com/qdoqcyp.png" />
<img src="https://imgur.com/ezUISdQ.png" />
<img src="https://imgur.com/zsYDCeT.png" />

```
When accepted two fields with randomized ships' positions are created. 
You can shoot by clicking on fields. When all ships are shot game is over and deleted from database.
```

```
After first turn:
```

<img src="https://imgur.com/vESbbMo.png" />

# Author
<a href="https://www.linkedin.com/in/stephen-stanbridge-26bbb416a/"> Stephen Stanbridge</a>
