# Hosting Apptainer SIF files on Quay.io

This guide covers hosting Apptainer SIF container images for Omnibenchmark on Quay.io using ORAS.

---

## What is ORAS?

**ORAS** (OCI Registry As Storage) allows storing arbitrary artifacts (like Apptainer SIF files) in OCI-compliant container registries.

---

## Initial setup

### 1. Create a Quay.io account

1. Go to [https://quay.io/](https://quay.io/) and click **Sign In**
2. Click **Register for Red Hat account** and make sure to create a **personal account**
3. Confirm your email address and accept terms
4. You'll now have access to [https://quay.io/repository/](https://quay.io/repository/)

### 2. Join the Omnibenchmark org

Contact **Izaskun** or **Ben** to be added to the Omnibenchmark organization on Quay.io.

---

## Repository setup

### 3. Create a new repository (for specific environment)

1. Navigate to the Omnibenchmark organization on Quay.io
2. Click **Create New Repository**
3. Choose descriptive name matching benchmark and environment
4. **Set visibility to Public**
5. Click **Create Repository**

**Note:** If adding to an existing repository, skip to robot setup.

### 4. Create a robot for pushing

Robot accounts provide secure, programmatic access for CI/CD and automated pushes.

1. Go to the org repository page
2. Navigate to **Settings** → **Robot Accounts**
3. Click **Create Robot Account**
4. Choose **Create Organization Robot** (not a personal robot)
5. Set a descriptive name (e.g., `push`)
6. Grant **Write** permissions
7. Click **Create**
8. **Save the token immediately** (will be used for login)

---

## Pushing SIF Images

### 5. Login to Quay.io

Use the robot account credentials to authenticate:

```bash
apptainer registry login --username 'omnibenchmark+push' docker://quay.io
```

When prompted, enter the robot account token as the password.

### 6. Push Your SIF Image

Use the ORAS protocol to push your image:

```bash
apptainer push <your-image>.sif oras://quay.io/omnibenchmark/<repo-name>:<tag>
```

**Example:**
```bash
apptainer push scanpy_full.sif oras://quay.io/omnibenchmark/scrna-bench:2026-01-09
```

**Tag Conventions:**
- Date format shown: `YYYY-MM-DD`
- Other tags: `latest`, `v1.0`, `stable`, etc.

### 7. Verify Upload

Pull the image to verify it was uploaded correctly:

```bash
apptainer pull oras://quay.io/omnibenchmark/<repo-name>:<tag>
```

This will download the image as `<repo-name>_<tag>.sif` in your current directory.

**Note on filenames:** The registry stores images by repository path and tag, not by filename. When you pull, Apptainer auto-generates a filename from the repo and tag. To specify a custom output filename, use: `apptainer pull <desired-name>.sif oras://quay.io/...`

---

## Updating Existing Images

To update an image with the same tag (e.g., fixing a bug in `latest`):

1. Rebuild your SIF file locally
2. Push with the same tag - this will **overwrite** the existing image:

```bash
apptainer push scanpy_full.sif oras://quay.io/omnibenchmark/scrna-bench:latest
```

---

## Summary Workflow

```bash
# 1. Login (one-time per session)
apptainer registry login --username 'omnibenchmark+push' docker://quay.io

# 2. Build your container
apptainer build myimage.sif myimage.def

# 3. Push to Quay
apptainer push myimage.sif oras://quay.io/omnibenchmark/my-repo:tag

# 4. Verify
apptainer pull oras://quay.io/omnibenchmark/my-repo:tag
```

---

## Notes

- **Public repositories are free** on Quay.io
- **Robot accounts** are organization-level, shared across repositories within Omnibenchmark
- **Multiple tags** can point to the same image (useful for `latest` + versioned tags)
