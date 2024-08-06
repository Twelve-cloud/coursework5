#! /bin/bash
# master
kubectl exec -i test-statefulset-0 -n deploy -- bash << EOF
echo "wal_level = logical" >> /var/lib/postgresql/data/postgresql.conf
echo "host StockTrader all test-statefulset-1.service-database-headless.deploy.svc.cluster.local trust" >> /var/lib/postgresql/data/pg_hba.conf
echo "host StockTrader all test-statefulset-2.service-database-headless.deploy.svc.cluster.local trust" >> /var/lib/postgresql/data/pg_hba.conf
su - postgres
pg_ctl restart -D /var/lib/postgresql/data
EOF
sleep 10 && kubectl wait --for=condition=Ready pod/test-statefulset-0 -n deploy --timeout=-30s
kubectl exec -i test-statefulset-0 -n deploy -- bash << EOF
PGPASSWORD=Annieleo1! pg_dumpall --database=postgres --host=test-statefulset-0.service-database-headless.deploy.svc.cluster.local --username=Twelve --globals-only --no-privileges | psql -U Twelve StockTrader
exit
EOF

# replica1
kubectl exec -i test-statefulset-1 -n deploy -- bash << EOF
echo "wal_level = logical" >> /var/lib/postgresql/data/postgresql.conf
su - postgres
pg_ctl restart -D /var/lib/postgresql/data
EOF
sleep 10 && kubectl wait --for=condition=Ready pod/test-statefulset-1 -n deploy --timeout=-30s
kubectl exec -i test-statefulset-1 -n deploy -- bash << EOF
PGPASSWORD=Annieleo1! pg_dump --dbname=StockTrader --host=test-statefulset-0.service-database-headless.deploy.svc.cluster.local --username=Twelve --create --schema-only | psql -U Twelve StockTrader
exit
EOF


# replica2
kubectl exec -i test-statefulset-2 -n deploy -- bash << EOF
echo "wal_level = logical" >> /var/lib/postgresql/data/postgresql.conf
su - postgres
pg_ctl restart -D /var/lib/postgresql/data
EOF
sleep 10 && kubectl wait --for=condition=Ready pod/test-statefulset-2 -n deploy --timeout=-30s
kubectl exec -i test-statefulset-2 -n deploy -- bash << EOF
PGPASSWORD=Annieleo1! pg_dump --dbname=StockTrader --host=test-statefulset-0.service-database-headless.deploy.svc.cluster.local --username=Twelve --create --schema-only | psql -U Twelve StockTrader
exit
EOF

# master
kubectl exec -i test-statefulset-0 -n deploy -- bash << EOF
su - postgres << EOF
psql -U Twelve StockTrader << EOF
CREATE PUBLICATION db_pub FOR ALL TABLES;
\q
exit
exit
EOF

# replica1
kubectl exec -i test-statefulset-1 -n deploy -- bash << EOF
su - postgres
psql -U Twelve StockTrader << EOF
CREATE SUBSCRIPTION db_sub_replica1 CONNECTION 'host=test-statefulset-0.service-database-headless.deploy.svc.cluster.local dbname=StockTrader user=Twelve password=Annieleo1!' PUBLICATION db_pub;
\q
exit
exit
EOF

# replica2
kubectl exec -i test-statefulset-2 -n deploy -- bash << EOF
su - postgres
psql -U Twelve StockTrader << EOF
CREATE SUBSCRIPTION db_sub_replica2 CONNECTION 'host=test-statefulset-0.service-database-headless.deploy.svc.cluster.local dbname=StockTrader user=Twelve password=Annieleo1!' PUBLICATION db_pub;
\q
exit
exit
EOF