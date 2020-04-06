cd ~/cse6242-2020-TeamProject/

rm -rf cse6242-2020-TeamProject/

git clone https://github.gatech.edu/jinness3/cse6242-2020-TeamProject.git

gzip -d /home/teamelevenproject/cse6242-2020-TeamProject/cse6242-2020-TeamProject/WebFront/static/center_distances_final.csv.gz

cd /home/teamelevenproject/cse6242-2020-TeamProject/cse6242-2020-TeamProject/WebFront

gcloud app deploy
