FROM alpine:latest

RUN apk update  \
    && apk add curl bash unzip

RUN curl -fsSL https://clis.cloud.ibm.com/install/linux | sh \
    && ibmcloud -v \
    && ibmcloud plugin install cloud-object-storage \
    && ibmcloud plugin list

CMD ["/bin/bash"]
