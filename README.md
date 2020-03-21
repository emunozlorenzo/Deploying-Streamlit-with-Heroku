<p align="center"> 
<img src="https://github.com/emunozlorenzo/MasterDataScience/blob/master/img/image2.png">
</p>

# Deploying a Streamlit Dashboard with Heroku

![alt text](https://github.com/emunozlorenzo/MasterDataScience/blob/master/img/icon2.png "Logo Title Text 1") [Eduardo Muñoz](https://www.linkedin.com/in/eduardo-mu%C3%B1oz-lorenzo-14144a144/)


1. Build your App

```py
import streamlit as st
import pandas as pd
import numpy as np

def main():
# Your Code
if __name__ == "__main__":
    main()
```

2. Test your App (Local Environment)

```sh
~$ streamlit run app.py
```

3. Create your requeriments.txt file

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

4. Setup.sh and Procfile

Heroku needs these files for starting the app

