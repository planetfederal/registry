FROM openjdk:8-jdk
#FROM ubuntu:14.04

#ENV DEBIAN_FRONTEND=noninteractive
#
#RUN apt-get update && apt-get install -y --no-install-recommends software-properties-common unzip && add-apt-repository -y ppa:webupd8team/java && \
#    apt-get update && \
#    (echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | sudo /usr/bin/debconf-set-selections) && \
#    apt-get install --no-install-recommends -y oracle-java8-installer && \
#    rm -rf /var/cache/oracle-jdk8-installer && \
#    echo "networkaddress.cache.ttl=60" >> /usr/lib/jvm/java-8-oracle/jre/lib/security/java.security && \
#    apt-get clean && rm -rf /var/lib/apt/lists/*
#ENV JAVA_HOME /usr/lib/jvm/java-8-oracle

# es cant be runned by root
RUN groupadd -g 1000 elasticsearch && useradd elasticsearch -u 1000 -g 1000

RUN mkdir -p /usr/src/downloads
WORKDIR /usr/src/downloads

# building o19s elasticsearch feature/heatmap, only works with gradle 2.13
RUN wget "https://services.gradle.org/distributions/gradle-2.13-all.zip" \
	&& wget "https://github.com/sstults/elasticsearch/archive/master.zip" \
	&& unzip "gradle-2.13-all.zip" \
	&& unzip "master.zip"

WORKDIR /usr/src/downloads/elasticsearch-master
RUN ../gradle-2.13/bin/gradle assemble

RUN mkdir -p /opt/elasticsearch && \
    tar zxvf distribution/tar/build/distributions/elasticsearch-6.0.0-alpha1-SNAPSHOT.tar.gz -C /opt/elasticsearch --strip-components=1

WORKDIR /opt/elasticsearch
COPY config ./config
RUN set -ex && for path in data logs config plugins config/scripts; do \
        mkdir -p "$path"; \
        chown -R elasticsearch:elasticsearch "$path"; \
    done

USER elasticsearch
ENV PATH=$PATH:/opt/elasticsearch/bin
CMD ["elasticsearch"]

EXPOSE 9200 9300