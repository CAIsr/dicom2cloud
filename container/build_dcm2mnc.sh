
imageName='dcm2mnc'
buildDate=`date +%Y%m%d`

docker build -t ${imageName}:$buildDate -f  Dockerfile.${imageName} .

#test:
#docker run -it ${imageName}:$buildDate
#exit 0

#docker run --rm -itd --name ${imageName}_reprozip --security-opt=seccomp:unconfined ${imageName}:$buildDate


#ZIP IMAGE
#cmd1="/home/neuro/run.sh"
#neurodocker reprozip trace ${imageName}_reprozip "$cmd1" 
#reprounzip docker setup neurodocker-reprozip.rpz test

#docker run -it ${imageName}:$buildDate


#Tag and push online
docker tag ${imageName}:$buildDate caid/${imageName}:$buildDate
#docker login
docker push caid/${imageName}:$buildDate
docker tag ${imageName}:$buildDate caid/${imageName}:latest
docker push caid/${imageName}:latest


