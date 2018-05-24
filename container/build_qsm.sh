
imageName='qsm'
buildDate=`date +%Y%m%d`

docker build -t ${imageName}:$buildDate -f  Dockerfile.${imageName} .

#test:
docker run -it ${imageName}:$buildDate
exit 0


#Tag and push online
docker tag ${imageName}:$buildDate caid/${imageName}:$buildDate
#docker login
docker push caid/${imageName}:$buildDate
docker tag ${imageName}:$buildDate caid/${imageName}:latest
docker push caid/${imageName}:latest
