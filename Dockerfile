FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Install additional PyQt5 packages
RUN apt-get update \
    && apt-get install -y \
        python3-pyqt5.qtopengl \
        python3-pyqt5.qtquick \
        # Install Qml
        libx11-xcb1 \
        libxcb-xinerama0 \
        libxcb-xkb \
        qmlscene \
        qml-module-*

# Copy the requirements file
COPY requirements.txt requirements.txt

# Install project dependencies
RUN pip install -r requirements.txt

# Copy the entire project into the container
COPY . /app

# Set the entry point
CMD ["python", "main.py"]
