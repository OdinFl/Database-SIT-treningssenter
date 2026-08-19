import functions
import user_interface

def main():
    db_sti = "db/data.db"
    schema_sti = "db/schema.sql"
    test_data_sti = "db/test_data.sql"

    # Slett databasen
    functions.slett_db(db_sti)

    # Initialiser schema
    with open(schema_sti, "r", encoding="utf-8") as f:
        schema = f.read()
    con = functions.opprett_database(db_sti, schema_sti)

    # Last inn data
    with open(test_data_sti, "r", encoding="utf-8") as f:
        test_data = f.read()

    functions.kjor_sql_file(con, test_data)

    # start brukergrensensitt
    user_interface.grensesnitt(con)
    con.close()

if __name__ == "__main__":
    main()
