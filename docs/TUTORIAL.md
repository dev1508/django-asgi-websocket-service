# Tutorial for Setting Up the Service

This Tutorial assumes MacOS developer environment.

## Pre-requisites

1. Install and start grafana.
   ```bash
   brew install grafana
   brew services start grafana 
   ```
2. Install prometheus.
   ```bash
   brew install prometheus
   ```
3. Either install Docker Desktop or colima.
   ```bash
   brew install docker colima
   colima start
   brew install docker-compose
   ```


---

## Clone the repo

```bash
git clone https://github.com/dev1508/django-asgi-websocket-service.git
```

---

## After Cloning

1. Open the repo in your preferred IDE and open terminal.
2. Setup virtualenv.
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies from requirements.txt.
   ```bash
   pip install -r requirements.txt
   ```
4. Move into /app directory.
   ```bash
   cd app
   ```

---

## Start the service

1. In terminal, inside /app, run this command:
   ```bash
   uvicorn core.asgi:application --host 127.0.0.1 --port 8000
   ```
2. In another terminal, run the following command:
   ```bash
   npx wscat -c ws://localhost:8000/ws/chat/
   ```
   It might ask you install wscat, enter 'y'. This sets up your websocket connection.
   1. You will see a console, enter any text message and hit enter. You will get the count of the text message.
   2. To exit the websocket connection, simply write 'quit' and hit enter.
3. You can do step 2 in multiple different terminals.

---

## Prometheus Set Up
 
   1. Open a new terminal.
   2. Head over to `django-asgi-websocket-service/prometheus`
   3. Run this command:
       ```bash
       prometheus --config.file=prometheus.yml
       ```
   4. Visit `http://localhost:9090/query` for running queries and checking alerts.

---

## Grafana Set Up

   1. Head over to `localhost:3000`.
   2. Username and password are both equal to _**admin**_.
   3. Click on "Data Your First Data Source" and select **Prometheus**.
   4. Go to + → Import and upload JSON placed at `./grafana/dashboards/ws_dashboard.json`.
   5. Graphs will be visible (though empty).
   6. The name of the variables for each graph is mentioned below:
      1. Active WebSocket Connections - `ws_active_connections`
      2. Total messages - `ws_total_messages_total`
      3. WebSocket Errors - `ws_error_count_total`
      4. Shutdown Duration - `ws_shutdown_duration_seconds_sum`


---

## Metrics - Observability

1. Run the following commands to check the metrics:
   1. **Error count**:
      ```bash
      curl http://localhost:8000/metrics | grep error_count
      ```
   2. **Total messages**:
      ```bash
      curl http://localhost:8000/metrics | grep total_messages
      ```
   3. **Active connections**:
      ```bash
      curl http://localhost:8000/metrics | grep active_connection
      ```
      

---

## Liveliness and Readiness

- **Liveliness**:
   ```bash
   curl http://localhost:8000/healthz
   ```
- **Readiness**:
   ```bash
   curl http://localhost:8000/readyz
   ```
  
---

## Monitoring

In another terminal, run the command: `./monitor.sh`

---

## Blue - Green Deployment

### Set Up
1. Start the service using:
   ```bash
   docker-compose down -v && docker-compose build && docker-compose up
   ```
2. When started, from another terminal, hit any request, for ex:
   ```bash
    curl http://localhost:8080/healthz # notice the port change
   ```
3. In the previous terminal, while checking logs, that the requests are getting served by `blue-app`.
   

### Switching between blue and green app

1. In some other terminal, run the command: `./promote.sh`. This will stop the current running app and start the other one.
2. Now again hit any request like before.
3. This time, in logs, the requests are getting served by `green-app`.

---

## Prometheus Alert Rule

1. Disconnect all the connections for 120 seconds.
2. Then navigate to the Alerts section in Prometheus UI.
3. It will be in _FIRING_ mode, showing that it is triggered.

---

## Performance

1. Start the service locally.
2. In one of the terminal, run: `python ./test_files/ws_load_test.py`
3. Also the service is starting under 3s and shutting under 10s.

---

## Github CI pipeline

1. When pushing any changes to Github, Github-Actions are getting triggered.

---

## Bonus Feature

### Reconnection Support
1. When starting the service and establishing a websocket connection, nonte the `Session ID` getting printed in the logs.
2. To reopen a closed ws connection, we can pass this `Session ID` as a query param, like:
   ```bash
   npx wscat -c ws://localhost:8000/ws/chat/?session_id=<some-uuid>
   ```

---

## Author's Comments

1. For the reconnection, ideally, Redis should be used. In the current project, I have used in-memory. Redis would have solved the reconnection support, even after switching traffic. 
2. Canary Deployment would be a better choice when traffic is higher than 5000.

---

Thanks. 
Let's connect here: [LinkedIn](https://www.linkedin.com/in/dev-vrat-pathak-aa6570176/)