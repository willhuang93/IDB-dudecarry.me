eval SWE_CLUSTER_PATH=~/carina_creds/docker.env
echo ${SWE_CLUSTER_PATH}

if [ ! -f "${SWE_CLUSTER_PATH}" ]
then
    echo "ERROR: ~/carina_creds not found, download them from slack or getcarina.com"
    exit 1
fi

source ${SWE_CLUSTER_PATH}

export DOCKER_HOST="${DOCKER_HOST%:2376}:42376"

# fix an issue with windows path for certificate file
if [ "$(expr substr $(uname -s) 1 5)" == "MINGW" ];
then
    export DOCKER_CERT_PATH=$(echo $DOCKER_CERT_PATH | sed 's#\/##1' | sed 's#\/#:\/#1')
fi

