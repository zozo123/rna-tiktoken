import pandas as pd
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.engine.url import URL
from sqlalchemy import inspect
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import csv


def get_db_params():
    return {
        "drivername": "postgresql+psycopg2",
        "username": "postgres",
        "password": "new_password",
        "host": "localhost",
        "port": "5433",
        "database": "RNACENETRAL",
    }


def explore_database():
    db_params = get_db_params()
    connection_string = URL.create(**db_params)
    engine = create_engine(connection_string)

    inspector = inspect(engine)
    schema_name = "rnacen"

    tables = inspector.get_table_names(schema=schema_name)
    print(f"Tables in {schema_name} schema of RNACENETRAL:")
    for table in tables:
        print("-", table)
    print()

    for table in tables:
        print(f"Columns in '{table}' table:")
        columns = inspector.get_columns(table, schema=schema_name)
        for column in columns:
            print(f"- {column['name']} ({column['type']})")
        print()

    if "rna" in tables:
        print("Columns in 'rna' table:")
        columns = inspector.get_columns("rna", schema=schema_name)
        for column in columns:
            print(f"- {column['name']} ({column['type']})")
        print()

        with engine.connect() as connection:
            result = connection.execute(f"SELECT * FROM {schema_name}.rna LIMIT 5;")
            print("First 5 rows of 'rna' table:")
            for row in result:
                print(row)
            result = connection.execute(f"SELECT COUNT(*) FROM {schema_name}.rna;")
            print(f"Number of rows in 'rna' table: {result.fetchone()[0]}")
            result = connection.execute(f"SELECT DISTINCT len FROM {schema_name}.rna;")
            lengths = {row[0]: 0 for row in result}
            result = connection.execute(
                f"SELECT len, COUNT(*) FROM {schema_name}.rna GROUP BY len;"
            )

            for row in result:
                lengths[row[0]] = row[1]

            print(
                f"Number of different lengths of RNA sequences: {len(lengths)}, sum of all the counts: {sum(lengths.values())}"
            )

            MIN_FREQ = 10
            lengths = {
                length: lengths[length]
                for length in lengths
                if lengths[length] > MIN_FREQ
            }

            print(
                f"Number of different lengths of RNA sequences with count > {MIN_FREQ}: {len(lengths)}, sum of all the counts: {sum(lengths.values())}"
            )

            print("Number of sequences with each length:")
            for length in sorted(lengths.keys()):
                print(f"- {length}: {lengths[length]}")
            print()

            length_values = list(lengths.keys())
            frequencies = list(lengths.values())

            plt.style.use("seaborn-whitegrid")

            plt.figure(figsize=(10, 10))
            plt.hist(
                length_values,
                weights=frequencies,
                bins=len(length_values),
                density=True,
                cumulative=True,
                histtype="stepfilled",
                alpha=0.8,
            )
            plt.xlabel("Length of RNA sequence")
            plt.ylabel("Probability")
            cdf_filename = "./rna_lengths_cdf.png"
            plt.savefig(cdf_filename)
            plt.show()

            plt.figure(figsize=(10, 10))
            plt.hist(
                length_values,
                weights=frequencies,
                bins=50,
                density=True,
                alpha=0.8,
            )
            plt.xlabel("Length of RNA sequence")
            plt.ylabel("Density")
            pdf_filename = "./rna_lengths_pdf.png"
            plt.savefig(pdf_filename)
            plt.show()

            csv_filename = "./rna_central_sequences.csv"
            query = f"SELECT seq_short FROM {schema_name}.rna;"

            with open(csv_filename, "w", newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["len", "sequence"])

                count_null = 0
                count_chunck = 0

                results = connection.execution_options(stream_results=True).execute(
                    query
                )
                for row in results.yield_per(100):
                    count_chunck += 1
                    if not row or not row[0]:
                        count_null += 1
                        continue

                    writer.writerow([len(row[0]), row[0]])
                print(f"Number of null sequences: {count_null}")
                print(f"Number of chuncks: {count_chunck}")
    else:
        print(
            f"'rna' table does not exist in the {schema_name} schema of RNACENETRAL database!"
        )


if __name__ == "__main__":
    """
    1. Download the RNACentral Database
        The RNACentral database can be downloaded from the RNACentral website. The database is available in various formats such as MySQL, PostgreSQL, and SQLite. Choose the one that suits your needs.
        Here is the link to the download page: https://rnacentral.org/help/download

    2. Install PostgreSQL
        If you choose to download the PostgreSQL version of the database, you will need to have PostgreSQL installed on your machine. You can download it from the official PostgreSQL website.
        Here is the link to the download page: https://www.postgresql.org/download/

    3. Import the Database
        Once you have PostgreSQL installed, you can import the RNACentral database using the pg_restore command. The command might look something like this:
        pg_restore -U username -d dbname -1 /path/to/your/database/dump

    4. Run the Database
        After importing the database, you can run it using the psql command:
        psql -U username -d dbname
        Replace username with your PostgreSQL username and dbname with the name of the database.
    """
    explore_database()
