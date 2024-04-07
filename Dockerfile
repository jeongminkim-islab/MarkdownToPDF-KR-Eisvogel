# Start from the pandoc/extra image based on Ubuntu
FROM pandoc/extra:latest-ubuntu

# Avoid prompts by apt-get by setting this environment variable
ENV DEBIAN_FRONTEND=noninteractive

# Install Python, pip, and necessary packages including tzdata
RUN apt-get update && \
    apt-get install -y python3 python3-pip texlive-xetex texlive-fonts-recommended texlive-plain-generic fonts-noto-cjk tzdata fonts-nanum && \
    # Automatically configure the timezone
    ln -fs /usr/share/zoneinfo/Asia/Seoul /etc/localtime && dpkg-reconfigure --frontend noninteractive tzdata && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip3 install --upgrade pip

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the application's requirements.txt and install Python dependencies
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application's source code
COPY . /usr/src/app

# Expose the port the app runs on
EXPOSE 8080

# 기본 ENTRYPOINT를 제거합니다.
ENTRYPOINT []

# Define the command to run the Flask application
CMD ["python3", "app.py"]
