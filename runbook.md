# Runbook: Database Connectivity Failure (RB-01)

**ID**: RB-01  
**Title**: Database Connectivity Failure Recovery  
**Service**: E-Commerce Checkout System (Database Service)  
**Severity**: Critical (SEV-1)  
**Author**: DevOps Team  

---

## 1. Trigger (觸發條件)
- **Alert**: `DatabaseConnectionError`
- **Symptom**: 
  - Checkout page shows "Service Unavailable" or "System Error".
  - Grafana "Error Rate" spikes to > 5%.
  - Logs show `psycopg2.OperationalError: could not connect to server`.

## 2. Diagnosis (診斷步驟)

### Step 2.1: Check Container Status
Check if the database container is running.
```bash
docker ps | grep ecommerce-db
```
*Expected Output*: You should see a container named `ecommerce-db` with status `Up`.
*If Empty or Exited*: The container has crashed or stopped.

### Step 2.2: Check Logs
Inspect the database logs for errors.
```bash
docker logs ecommerce-db --tail 50
```
Look for "FATAL", "PANIC", or "OOM Killed".

## 3. Mitigation / Recovery (復原步驟)

### Step 3.1: Restart Database Container
If the container is stopped or stuck, restart it.
```bash
docker start ecommerce-db
```
OR if it's unresponsive:
```bash
docker restart ecommerce-db
```

### Step 3.2: Verify Connectivity
Wait for 10-15 seconds for the database to initialize.
Check if the application can connect again.
```bash
# Check app logs for successful connection or lack of errors
docker logs <app-container-id> --tail 20
```

## 4. Verification (驗證)
1. Access the Checkout Page (`http://localhost:5000`).
2. Try to place a test order.
3. Check the Observability Dashboard (`http://localhost:5000/dashboard/observability-dashboard.html`) to ensure "System Health" returns to normal and "Error Rate" drops to 0%.

## 5. Escalation (升級流程)
If the database fails to start or crashes immediately after restart:
1. Check disk space (`df -h`).
2. Contact the Database Reliability Engineer (DBRE) on Slack channel `#ops-database`.
