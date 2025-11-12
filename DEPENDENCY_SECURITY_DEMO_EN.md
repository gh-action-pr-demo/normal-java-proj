---
theme: default
class: text-center
highlighter: shiki
lineNumbers: false
info: |
  ## GitHub Dependabot Dependency Security Check Configuration Demo
drawings:
  persist: false
transition: slide-left
title: GitHub Dependabot Dependency Security Check
mdc: true
marp: true
---

# 1. Background

## Problem
How to ensure the security of project dependencies? Vulnerability detection

## Expected Goals
- Automatic dependency vulnerability detection
- Real-time PR-level checks
- Flexible control of check process
- Automatic creation of fix PRs

---

# 2. Alternative Solutions

---

## 2.1 Custom Rules + GitHub Actions

- Hard to maintain ❌
- Supports allowlist/denylist ✅

## 2.2 Maven Plugin + GitHub Actions

- OWASP vulnerability detection plugin
  * Public service has rate limits ❌
  * Requires API key application
- Can suggest target upgrade versions ✅

---

## 2.3 Dependabot + dependency-review-action

### ✅ Advantages
- PR-level real-time checks
- Detailed vulnerability reports and fix suggestions
- Label-based check skip control
- Dependabot automatically creates fix PRs
- Simple configuration, easy to maintain

### ❌ Disadvantages
- Requires manual workflow configuration
- Dependency review action may not show target versions in comments (but Dependabot PRs include fix version suggestions)

---

## 2.3.1 Implementation Results

1. **Trigger Conditions**
   - PR creation/update
   - Label addition/removal

2. **Check Process**
   - Check if `dependency-check-ignore` label exists
   - Has label → Skip check, create successful Check
   - No label → Execute dependency check

3. **Result Handling**
   - Has vulnerabilities → Create failed Check + detailed report comment
   - No vulnerabilities → Create successful Check + no vulnerability comment

---

# 3. How to Configure

---

## 3.1 dependency-review-action

- Enables PR-level checks
- Provides label-based control to skip checks
- Outputs detailed reports in PR comments

```yaml
# .github/workflows/dependency-review.yml
on:
  pull_request:
    types: [opened, synchronize, reopened]
  issues:
    types: [labeled, unlabeled]

jobs:
  dependency-review:
    steps:
      - uses: actions/dependency-review-action@v4
      - # Check labels and create comments
```

---

## 3.2 Dependabot

- Automatically checks dependencies and creates upgrade PRs
- **Important**: Configuration file (`dependabot.yml`) must be on the default branch (master/main)
- Scheduled execution (configurable: daily/weekly/monthly)

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "maven"
    schedule:
      interval: "weekly"
    groups:
      spring-boot-dependencies: # PR grouping - multiple dependencies in one PR
        patterns:
          - "org.springframework.boot:*"
        update-types:
          - "minor"
          - "patch"
```

---

# 4. GitHub Actions Implementation Principles

---

## 4.1 GitHub Dependabot Implementation Principles

1. **Dependency Graph Generation**
   - GitHub automatically scans repositories, generates dependency graphs, stores in GitHub database
   - Integrates multiple security databases (CVE, GHSA, etc.)
   - Real-time vulnerability information updates

2. **Automatic Detection**
   - Compare dependency versions with vulnerability database
   - Discover matching vulnerabilities
   - Create Dependabot Alerts

3. **Automatic Fix**
   - Find fix versions
   - Create fix PRs
   - Automatically update dependencies (manual approval required)

---

## 4.1.1 Dependabot FAQ

- **Configuration must be on default branch (`master`/`main`)**: Dependabot reads configuration from the default branch and creates PRs targeting it

- **Only one PR per dependency**: Dependabot won't create duplicate PRs for the same dependency. If a PR exists, it will be updated instead

- **PR limit control**: `open-pull-requests-limit` limits the total number of open PRs. Security updates are exempt from this limit

- **Auto-update existing PRs**: If a dependency has a newer version available, Dependabot updates the existing PR instead of creating a new one

- **Auto-close when manually fixed**: If you manually update a dependency in a dev branch and merge to `master`, Dependabot will automatically close the related PR on the next check

---

## 4.2 GitHub Dependency Review Implementation Principles

### Dependency Graph API
- Compare dependency changes between two commits
- Returns newly added/removed dependencies
- Returns version changes and associated vulnerability information
- Returns fix version suggestions

**Limitations**
- By default only shows newly introduced vulnerabilities
- Requires `security-events: read` permission

---

# 5. Demo

- Automatic dependency check and detailed report output in PR comments
- Add `dependency-check-ignore` label to skip checks
  * Label addition/removal automatically triggers the workflow

---

# 6. TODO / Future Improvements

- **Configuration distribution**: Batch deployment of configurations across hundreds of repositories

- **Enhanced control**: Skip check (implemented) vs. Force check
  - **Fine-grained control**: Enforce mandatory upgrades for critical dependencies

- **Organization-level reporting**: 
  - Vulnerability statistics dashboard
  - Upgrade action execution reports
  - Compliance tracking

---

## End

