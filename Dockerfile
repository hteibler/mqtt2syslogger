FROM python:3.12-rc-slim
WORKDIR /
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./*.py /
RUN adduser --system --group --no-create-home appuser
USER appuser
CMD python3 /syslogger.py
