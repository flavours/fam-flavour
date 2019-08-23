FROM alpine:3.9

# Version of the addon manager
ARG VERSION=0.1

ENV FAM_IDENTIFIER flavour/fam-flavour:$VERSION

RUN mkdir /app
WORKDIR /app 

# install confest for policies check
RUN wget https://github.com/instrumenta/conftest/releases/download/v0.6.0/conftest_0.6.0_Linux_x86_64.tar.gz
RUN tar xzf conftest_0.6.0_Linux_x86_64.tar.gz
RUN mv conftest /usr/local/bin
RUN rm conftest_0.6.0_Linux_x86_64.tar.gz

RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

# copy requirements
RUN mkdir -p /flavour/fam-flavour/
COPY requirements.txt /flavour/fam-flavour/requirements.txt
RUN pip install -r /flavour/fam-flavour/requirements.txt

# copy policies
RUN mkdir -p /flavour/fam-flavour/policy
COPY policy/*.rego /flavour/fam-flavour/policy/


COPY bin/add.py /bin/add
COPY bin/remove.py /bin/remove
COPY bin/check.py /bin/check
