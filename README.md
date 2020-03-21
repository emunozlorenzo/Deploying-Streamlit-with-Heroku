<p align="center"> 
<img src="https://github.com/emunozlorenzo/MasterDataScience/blob/master/img/image2.png">
</p>

# Deploying a Streamlit Dashboard with Heroku

![alt text](https://github.com/emunozlorenzo/MasterDataScience/blob/master/img/icon2.png "Logo Title Text 1") [Eduardo Muñoz](https://www.linkedin.com/in/eduardo-mu%C3%B1oz-lorenzo-14144a144/)

1. Create a Git Repo

_Note: Heroku allows deployment using Git or Docker._

```sh
git init
```

2. Build your App

```py
import streamlit as st
import pandas as pd
import numpy as np

def main():
# Your Code
if __name__ == "__main__":
    main()
```

3. Test your App (Local Environment)

```sh
~$ streamlit run app.py
```

4. Create your requeriments.txt file

This file contains the libraries that your code needs to work. To do this, you can use ```pipreqs```.

```sh
pipreqs /path/to/your/app/
```
After this command, a requirements.txt will be created in the folder of your app

```
matplotlib==3.1.0
streamlit==0.56.0
pandas==1.0.2
seaborn==0.9.0
numpy==1.16.3
```

5. Setup.sh and Procfile

Heroku needs these files for starting the app

    - setup.sh : create a streamlit folder with both credentials.toml and config.toml files.
    - Procfile : This file executes the setup.sh and then call streamlit run to run the app

```sh
# Setup.sh
mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
```
```sh
# Procfile
web: sh setup.sh && streamlit run app.py
```

6. Create a Heroku Account

Create a free account

7. Install Heroku CLI

[Follow these steps](https://devcenter.heroku.com/articles/getting-started-with-python#set-up)

8. Login into Heroku CLI

Move to your App folder and execute ```heroku login```

9. Deploy the App

Deploy your app by running ```heroku create``` in your app folder

10. Check it

Check your app by running ```heroku ps:scale web=1```

After that, push your code

```sh
git add .
git commit -m "message"
git push heroku master
```

11. Open it

Open your app using ```heroku open```