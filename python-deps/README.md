# Python Dependencies

This folder contains the Python web application components:

- `app.py` - Flask web application
- `requirements.txt` - Python dependencies
- `Dockerfile` - Container configuration

## To run the web application locally:

```bash
pip install -r requirements.txt
python app.py
```

## To run with Docker:

```bash
docker build -t pdf-webapp .
docker run -p 5000:5000 pdf-webapp
```
