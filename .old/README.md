
# DB Lab 1

### To run lab 1 solution:
1. Clone repository (master branch, tag "lab1")

2. To get full/test data, either execute ```git lfs pull``` or download data from  https://drive.google.com/drive/folders/116MZEg_GFvkl4zNM76dK_yjFKPJG78rd?usp=sharing There are 2 sample data sets. full19.csv and full20.csv are original files from ZNO web-site (733112 records total). test19.csv and test20.csv are test data (10000 records total), subset of full files. Select data set (full or test) and rename files to "d19.csv" and "d20.csv". Place "d19.csv" and "d20.csv" into data directory in repo root.

3. cd into deploy directory, run "recreate-external-volumes.sh" with admin privileges:

```
chmod +x ./recreate-external-volumes.sh
sudo ./recreate-external-volumes.sh
```

   The script recreates (remove old + create new) all required external volumes. Solution uses external volumes to demonstrate caching / fault tolerance.

4. Execute solution:

```
sudo docker compose up
```

5. Feel free to stop-start any of containers in compose: solution should recover after app and db containers are started again (tested app stop-start, db stop-start, both stop-start).
6. After solution is finished running, you should have 1 running container - db container. To check if data was written, run:

```
sudo docker exec -it 'db container id' bash
su postgres
psql
select count(*) from Zno;
```

sql query result should be 10000 for test data, 733112 for full data.

7. To see result of "Порівняти середній бал учасників з української мови та літератури у кожному регіоні у 2020 та 2019 роках серед тих кому було зараховано тест", run:

```
sudo docker run -it -e bash --mount source=deploy_app-output,target=/app-output,readonly alpine
cd app-output
ls -al
cat compare-"latest datetime".csv
```

**You can also find an example output for full data in ./data/output-full.csv**

8. To rerun solution with no cache, execute:

```
sudo docker compose down
sudo ./recreate-external-volumes.sh
sudo docker compose up
```