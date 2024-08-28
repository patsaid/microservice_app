#!/bin/bash

# Create a directory for the certificates
mkdir -p certs
cd certs

# Generate the CA private key without a passphrase
openssl genpkey -algorithm RSA -out ca.key

# Generate the CA certificate
openssl req -x509 -new -nodes -key ca.key -sha256 -days 3650 -out ca.pem \
  -subj "/C=US/ST=CA/L=San Francisco/O=YourCompany/OU=IT/CN=127.0.0.1"

# Generate the private key for your server certificate
openssl genpkey -algorithm RSA -out cert.key

# Generate a certificate signing request (CSR)
openssl req -new -key cert.key -out cert.csr \
  -subj "/C=US/ST=CA/L=San Francisco/O=YourCompany/OU=IT/CN=127.0.0.1"

# Sign the CSR with your CA certificate to get the final certificate
openssl x509 -req -in cert.csr -CA ca.pem -CAkey ca.key -CAcreateserial -out cert.pem -days 365 -sha256

# Clean up the CSR
rm cert.csr
