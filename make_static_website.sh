# downloads files in a folder named www.calciosplashala.it
wget -E -m -p -k http://www.calciosplashala.it

# copy statics
cp -r calcio_splash/static www.calciosplashala.it/static

# convert links to static
grep -rl https://cdn-calciosplashala.s3.amazonaws.com www.calciosplashala.it | xargs sed -i '' s@https://cdn-calciosplashala.s3.amazonaws.com@/static@g
