# Create certificate authority
mkdir esdoc_testca
cd esdoc_testca
mkdir certs private
chmod 700 private
echo 01 > serial
touch index.txt
cp ../create_test_certs_openssl.cnf ./openssl.cnf

openssl req -x509 -config openssl.cnf -newkey rsa:2048 -days 365 -out cacert.pem -outform PEM -subj /CN=MyTestCA/ -nodes
openssl x509 -in cacert.pem -out cacert.cer -outform DER

# Create server certificate
cd ..
mkdir server
cd server
openssl genrsa -out key.pem 2048
openssl req -new -key key.pem -out req.pem -outform PEM -subj /CN=$(hostname)/O=server/ -nodes

cd ../esdoc_testca
openssl ca -config openssl.cnf -in ../server/req.pem -out ../server/cert.pem -notext -batch -extensions server_ca_extensions
cd ../server
openssl pkcs12 -export -out keycert.p12 -in cert.pem -inkey key.pem -passout pass:$1

# Create client certificate
cd ..
mkdir client
cd client
openssl genrsa -out key.pem 2048
openssl req -new -key key.pem -out req.pem -outform PEM -subj /CN=$(hostname)/O=client/ -nodes

cd ../esdoc_testca
openssl ca -config openssl.cnf -in ../client/req.pem -out ../client/cert.pem -notext -batch -extensions client_ca_extensions
cd ../client
openssl pkcs12 -export -out keycert.p12 -in cert.pem -inkey key.pem -passout pass:$1
cd ..