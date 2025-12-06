# Service Reliability Guide & Runbooks

**Project:** E-Commerce Checkout System
**Role:** Tester / SRE Team
**Last Updated:** 2025-11-29

---

## 1. Service Level Definitions (SLI / SLO / SLA)

### Service Level Indicators (SLIs)
We measure the reliability of the Checkout System using the following metrics:

1.  **Availability**: The percentage of HTTP requests that result in a non-5xx status code.
    *   *Formula*: `(Total Requests - 5xx Errors) / Total Requests * 100`
2.  **Latency**: The time taken to serve a successful HTTP request (measured at the Load Balancer).
    *   *Metric*: 95th percentile (P95) response time in milliseconds.
3.  **Error Rate**: The ratio of failed requests (HTTP 500/503) to total requests.

### Service Level Objectives (SLOs)
Our internal reliability targets to ensure user satisfaction:

| Metric | Target (SLO) | Time Window |
| :--- | :--- | :--- |
| **Availability** | **99.9%** | Rolling 30-day window |
| **Latency** | **< 200ms** (P95) | Rolling 1-hour window |
| **Error Rate** | **< 1%** | Rolling 5-minute window |

### Service Level Agreements (SLAs)
Our external commitment to customers (simulated):

> "We guarantee that the E-Commerce Checkout System will be available **99.5%** of the time during any monthly billing cycle. If we fail to meet this guarantee, customers are eligible for a 10% service credit."

---

## 2. Operational Runbooks

### RB-01: Database Connectivity Failure (Critical)

**Description**: The application cannot connect to the backend database, causing all checkout operations to fail (HTTP 503).

#### 1. Detecting an Incident
*   **Alert**: PagerDuty triggers "Critical: Database Service Down".
*   **Dashboard**:
    *   "System Health" drops below 50%.
    *   "Database" service indicator turns **RED**.
    *   "Error Rate" spikes to ~100%.
*   **Logs**: High volume of `ConnectionRefusedError` or `OperationalError`.

#### 2. Identifying Root Cause
1.  **Check Fault Status API**:
    Run the following command to check if a known fault is active:
    ```powershell
    curl http://localhost:5000/fault/status
    ```
    *   *If output contains `"database_down": true`*: The database fault injection is active.
    *   *If output is normal*: Check container logs (`docker logs db`) for crashes.

#### 3. Executing Recovery Commands
**Scenario A: Simulated Fault (Most Common)**
Execute the recovery API to restore database connectivity:

*   **PowerShell**:
    ```powershell
    $body = '{"fault_type": "database_down"}'
    Invoke-RestMethod -Uri "http://localhost:5000/fault/recover" -Method POST -Body $body -ContentType "application/json"
    ```

*   **cURL**:
    ```bash
    curl -X POST http://localhost:5000/fault/recover -H "Content-Type: application/json" -d "{\"fault_type\": \"database_down\"}"
    ```

**Scenario B: Real Container Crash**
If not a simulated fault, restart the service:
```powershell
# (Simulated command for this project context)
Restart-Service -Name "PostgreSQL"
# OR
python app.py # Restart the flask app if needed
```

#### 4. Validating Service Health
1.  **Dashboard Check**: Refresh the Observability Dashboard.
    *   Verify "Database" service is **GREEN**.
    *   Verify "Error Rate" drops to 0%.
2.  **Functional Test**:
    Run a smoke test to verify checkout works:
    ```powershell
    curl -I http://localhost:5000/
    ```
    *   *Expected*: `HTTP/1.1 200 OK`

#### 5. Escalation Path and Communication
*   **Communication**:
    *   Update Status Page to "Investigating" immediately upon detection.
    *   Update to "Monitoring" after recovery.
*   **Escalation**:
    *   **T+0 min**: On-Call Engineer (You) investigates.
    *   **T+15 min**: If unresolved, escalate to **DevOps Lead**.
    *   **T+30 min**: If data corruption suspected, escalate to **Database Architect**.

---

### RB-02: High Latency / Performance Degradation (Major)

**Description**: System response time exceeds acceptable limits (>500ms), causing poor user experience but not total failure.

#### 1. Detecting an Incident
*   **Alert**: "Warning: High Latency > 200ms".
*   **Dashboard**: "Avg Response Time" gauge turns **YELLOW** or **RED**.

#### 2. Identifying Root Cause
1.  Check `/fault/status` for `high_latency` flag.
2.  Check CPU/Memory usage on the host.

#### 3. Executing Recovery Commands
Remove the latency injection:

*   **PowerShell**:
    ```powershell
    $body = '{"fault_type": "high_latency"}'
    Invoke-RestMethod -Uri "http://localhost:5000/fault/recover" -Method POST -Body $body -ContentType "application/json"
    ```

#### 4. Validating Service Health
1.  Generate test traffic:
    ```powershell
    for ($i=1; $i -le 5; $i++) { curl http://localhost:5000/; Start-Sleep -Milliseconds 200 }
    ```
2.  Observe "Avg Response Time" on Dashboard returning to < 50ms.

#### 5. Escalation Path
*   **T+30 min**: If latency persists after recovery, escalate to **Backend Team** for code profiling.
