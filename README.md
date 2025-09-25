## Simple Chat Application

- Case study as well as project repo for Database Managament(23CSE202) build using **CockroachDB**.

## Note
- For Linux system :

    - Download the CockroachDB CA certificate (recommended)

    - In your CockroachDB Cloud console, go to your cluster → Connect → Download CA Cert.
      It will give you a cc-ca.crt or root.crt.

    - Save it in ~/.postgresql/ (that’s where psycopg2 looks by default):

    - mkdir -p ~/.postgresql
    - mv root.crt ~/.postgresql/root.crt

    - Then your .env should look like:

        **DATABASE_URL**=postgresql://<username>:<password>@<hostname>:26257/<dbname>?sslmode=verify-full&sslrootcert=/home/laptop-username/.postgresql/root.crt

