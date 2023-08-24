test:
	cd stocktrader && poetry run pytest
	cd stocktrader && flake8 .

run:
	kubectl create -f namespace.yaml
	kubectl wait --for jsonpath='{.status.phase}=Active' namespace/deploy --timeout=60s

	kubectl create -f service-account-deploy.yaml
	while ! kubectl get serviceaccount service-account-deploy -n deploy &> /dev/null; do echo "Waiting for service account. CTRL-C to exit."; sleep 1; done

	kubectl create -f resource-quota-deploy.yaml
	while ! kubectl get quota resource-quota-deploy -n deploy &> /dev/null; do echo "Waiting for resource qouta. CTRL-C to exit."; sleep 1; done

	kubectl create -f limit-range-deploy.yaml
	while ! kubectl get limits limit-range-deploy -n deploy &> /dev/null; do echo "Waiting for limit range. CTRL-C to exit."; sleep 1; done

	kubectl create -f secret-backend.yaml
	while ! kubectl get secret secret-backend -n deploy &> /dev/null; do echo "Waiting for secret-backend. CTRL-C to exit."; sleep 1; done

	kubectl create -f configmap-backend.yaml
	while ! kubectl get configmap configmap-backend -n deploy &> /dev/null; do echo "Waiting for configmap-backend. CTRL-C to exit."; sleep 1; done

	kubectl create -f service-backend.yaml
	while ! kubectl get service service-backend -n deploy &> /dev/null; do echo "Waiting for service-backend. CTRL-C to exit."; sleep 1; done

	kubectl create -f service-frontend.yaml
	while ! kubectl get service service-frontend -n deploy &> /dev/null; do echo "Waiting for service-frontend. CTRL-C to exit."; sleep 1; done

	kubectl create -f service-rabbitmq.yaml
	while ! kubectl get service service-rabbitmq -n deploy &> /dev/null; do echo "Waiting for service-rabbitmq. CTRL-C to exit."; sleep 1; done

	kubectl create -f service-database-headless.yaml
	while ! kubectl get service service-database-headless -n deploy &> /dev/null; do echo "Waiting for service-database-headless. CTRL-C to exit."; sleep 1; done

	kubectl create -f service-database-public.yaml
	while ! kubectl get service service-database-public -n deploy &> /dev/null; do echo "Waiting for service-database-public. CTRL-C to exit."; sleep 1; done

	kubectl create -f pv-database.yaml
	while ! kubectl get pv pv-database-0 pv-database-1 pv-database-2 &> /dev/null; do echo "Waiting for persistent volumes. CTRL-C to exit."; sleep 1; done

	kubectl create -f statefulset-database.yaml
	kubectl rollout status statefulset statefulset-database -n deploy

	kubectl create -f job-migrations.yaml
	kubectl wait --for=condition=complete job/job-migrations --timeout=-30s -n deploy

	chmod +x postgres-replication.sh
	./postgres-replication.sh

	kubectl create -f deployment-rabbitmq.yaml
	kubectl rollout status deployment deployment-rabbitmq -n deploy

	kubectl create -f deployment-backend.yaml
	kubectl create -f deployment-celery.yaml
	kubectl rollout status deployment deployment-backend -n deploy
	kubectl rollout status deployment deployment-celery -n deploy

	minikube addons enable metrics-server
	kubectl rollout status deployment metrics-server -n kube-system
	while ! kubectl top pod --all-namespaces &> /dev/null; do echo "Waiting for collecting metrics. CTRL-C to exit."; sleep 1; done

	kubectl create -f hpa-backend.yaml
	while ! kubectl get hpa hpa-backend -n deploy &> /dev/null; do echo "Waiting for hpa-backend. CTRL-C to exit."; sleep 1; done

	kubectl create -f hpa-celery.yaml
	while ! kubectl get hpa hpa-backend -n deploy &> /dev/null; do echo "Waiting for hpa-backend. CTRL-C to exit."; sleep 1; done

	kubectl create -f deployment-frontend.yaml
	kubectl rollout status deployment deployment-frontend -n deploy

start:
	minikube start

stop:
	minikube stop

delete:
	minikube delete