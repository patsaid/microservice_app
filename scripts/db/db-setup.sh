#!/bin/sh

# Set permissions for the certificate and key files
chown 70:70 /etc/ssl/certs/cert.key # 70:70 for alpine, 999:999 for debian
chmod 600 /etc/ssl/certs/cert.key

chmod 600 /etc/ssl/certs/cert.key
chmod 640 /etc/ssl/certs/cert.pem /etc/ssl/certs/ca.pem

# Ensure the correct ownership
chown postgres:postgres /etc/ssl/certs/cert.key /etc/ssl/certs/cert.pem /etc/ssl/certs/ca.pem

export PGUSER="postgres"
psql -c "CREATE DATABASE db;"

psql db -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"

# Enable the pgcrypto extension
psql db -c "CREATE EXTENSION IF NOT EXISTS pgcrypto;"