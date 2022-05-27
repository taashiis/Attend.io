
# Attend.io

A web interface to track attendance in offline session automatically along
with attendees' time of arrival using power of computer
vision.

This project is part of **Microsoft Engage 2022 Mentorship** program.

The project was made on Django frameowork. OpenCV and 
face-recognition libraries in python were used to code the backend
while HTML, CSS, Javascript along with Bootstrap library was used 
to code the front end of the webapp. SQLite was used
as database to store data.
## Authors

[Tanishqa Shital Singh](https://github.com/taashiis)

  Indraprastha Institute of  Information Technology Delhi (IIITD)
## Demo

https://youtu.be/tbvOatUv92E


## Run Locally

Clone the project

```bash
  git clone https://github.com/taashiis/Attend.io
```

Go to the project directory

```bash
  cd Attend.io
```

Install dependencies

```bash
  pip3 install -r requirements.txt
```

Start the server

```bash
  python3 manage.py runserver
```


## Documentation

[Documentation](https://drive.google.com/drive/folders/1srgk7MxdDNuXhVKup56Yncw_Rbgp2Tfv?usp=sharing)


## Error Fixing

On running `python3 manage.py runserver`, if you get error such as "
`dlib error: "symbol not found in flat namespace`

run :

```bash
  pip3 install dlib --force-reinstall --no-cache-dir --global-option=build_ext
```
    
On running `pip3 install -r requirements.txt`, if you get error such as "
`Building wheel for opencv-python (PEP 517) ... error`

run :

```bash
  pip install opencv-python==4.5.3.56 
```
or try earlier versions of openCV library