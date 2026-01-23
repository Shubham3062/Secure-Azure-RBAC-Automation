# Secure Azure RBAC Automation with Terraform & CI/CD

## Problem Statement

In real-world cloud environments, **access control** is one of the most critical yet most poorly managed areas.

Common problems that teams are facing:

* Manual role assignments in Azure Portal (error‑prone & non‑auditable)
* No approval trail for *who requested what and why*
* Over‑privileged users (security risk)
* No automation or consistency across environments

This project solves **all of the above** using a **policy‑driven, approval‑based, Terraform‑powered RBAC automation system**.

## What This Project Solves

This project provides:

* Controlled RBAC access using **pre‑approved JSON requests**
* Group‑based access (no direct user‑to‑role assignment)
* Policy validation before Terraform runs
* CI/CD‑driven enforcement using GitHub Actions
* Clean audit trail (who requested, who approved, when, why)

In short:

> **No approval → No access → No Terraform apply**

## High‑Level Architecture

1. User submits an **access request (JSON) for ease of project otherwise a JIRA ticket**
2. Request is validated against **roles.json + access policy rules**
3. Approved request is moved to `/approved/`
4. GitHub Actions triggers Terraform
5. Terraform assigns the Azure RBAC role to the **Azure AD group**

> Users are added to groups via Azure AD, Terraform only handles RBAC(Just like a core engine of the system).

## Key Files Explanation

### 1) `roles.json` – Role Catalog

Defines **what access is allowed** and under which conditions.

Example:

```json
"vm-reader-dev": {
  "azure_role_name": "Virtual Machine Reader",
  "allowed_environments": ["dev"],
  "allowed_employee_types": ["intern", "full_time"],
  "scope_type": "resource_group"
}
```

This prevents:

* Interns getting prod access
* Random roles being assigned

### 2) Access Request (Approved JSON)

Located at:

```
access-requests/approved/*.json
```

Example fields:

* Requester details
* Requested role
* Environment
* Duration
* Approval metadata

This file is the **single source of truth** for Terraform.

### 3) Terraform RBAC Module

Terraform:

* Reads approved request
* Resolves Azure role definition
* Assigns role to **Azure AD group**

No users are directly touched.

### 4) GitHub Actions CI/CD Pipeline

The pipeline:

1. Checks out the repo
2. Installs Python dependencies
3. Validates access request
4. Runs `terraform init`
5. Runs `terraform plan`
6. Runs `terraform apply`

This ensures **no human can bypass controls**.

## How to Test This Project in your environment(Step‑by‑Step)

### Step 1: Clone the Repository

```bash
git clone https://github.com/Shubham3062/Secure-Azure-RBAC-Automation.git
cd Secure-Azure-RBAC-Automation
```

### Step 2: Login to Azure

You must authenticate **before running Terraform**.

#### Option A – Azure CLI (recommended for local testing)

```bash
az login
az account set --subscription <SUBSCRIPTION_ID>
```

#### Option B – Service Principal (CI/CD)

Set these as **GitHub Secrets**:

* `ARM_CLIENT_ID`
* `ARM_CLIENT_SECRET`
* `ARM_TENANT_ID`
* `ARM_SUBSCRIPTION_ID`

### Step 3: Install Script Dependencies

```bash
pip install -r scripts/requirements.txt
```

### Step 4: Run Terraform Locally for testing the workflow

```bash
cd terraform
terraform init
terraform plan
```

> Make sure your account has **Owner or User Access Administrator** permissions.

### Step 5: CI/CD Testing via GitHub

1. Push code to GitHub and add secrets in your account.
2. Open **Actions** tab
3. Watch `terraform-rbac.yml` run
4. Verify role assignment in Azure Portal


## Security Best Practices Followed

* No secrets committed to GitHub
* No direct user role assignments
* roup‑based RBAC
* Approval‑driven access
* CI/CD enforcement
* Auditable JSON trail

## Who Should Use This Project

* Cloud / DevOps Engineers
* Security‑focused teams
* Students learning **real‑world Azure RBAC**
* Anyone preparing for **Azure + Terraform interviews**

Feel free to fork, adapt, and extend.

