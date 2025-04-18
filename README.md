## 1. Manual Setup 

### Step 1: Clone or copy the files

Make sure `pf_healthcheck.py` and `pf_analyze.py` are in the same folder (e.g. `~/path`).

### Step 2: Install dependencies

```bash
chmod +x code.sh
./code.sh
```

### Step 3: Run the monitor manually

```bash
python3 pf_healthcheck.py
```

### Step 4: Run the analysis

```bash
python3 pf_analyze.py
```

## 2. Setup using Ansible 


### Step 1: Navigate to the ansible folder

```bash
cd ansible/
```

### Step 2: Install dependencies and Run the deploy script

```bash
chmod +x run.sh
./run.sh
```

### Step 3: Checking if its running

```bash
chmod +x verify.sh
./verify.sh

```

### Generate a report from the CSV

```bash
chmod +x report.sh
./report.sh
```