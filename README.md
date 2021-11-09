## Nice code

Run `black .` and `isort .` from time to time in the root directory.

## Deploy to GCP

### Account setup

- Create an account at https://console.cloud.google.com/
- Create a new project
- Try create service in Cloud Run
- Enable billing
- Link billing

### Add service

- Create service in Cloud Run
- Select "Continuously deploy new revisions from a source repository"
- Set up with Cloud Build
- Enable Cloud Build API
- Choose GitHub as repository provider and authenticate
- Select repository
- `^master$` branch, Dockerfile
- Allow all traffic, allow unauthenticated invocations

### Custom domain

- Manage custom domains in Cloud Run
- Add mapping
- Verify a new domain
- Add subdomain

### Database

- Go to Firestore
- Select native mode

### Secrets & variables

- Go to Security -> Secret manager
- Enable
- Create secret
  - SECRET_KEY
- Enter secret value
  - Copy both 504-bit WPA Keys from https://randomkeygen.com/
- Go to service
- Edit & deploy new revision
- Variables & secrets
- Reference a secret
- SECRET_KEY, latest version, exposed as environment variable
- Done
- Add variable
- ALLOW_ORIGINS, http://localhost
- PRODUCT_REPOSITORY_BACKEND, firestore
- Deploy
- Fix error by adding a role to the secret in the secret manager
- Edit & deploy new revision
- Variables & secrets
- Deploy
