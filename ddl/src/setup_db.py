"""Setup a local sqlite database."""
import sqlite3

if __name__ == "__main__":
    DB_CONFIG = open("db_config", "r").read()
    con = sqlite3.connect(DB_CONFIG)
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS authors")
    cur.execute("DROP TABLE IF EXISTS books")
    cur.execute("DROP TABLE IF EXISTS authors_and_books")

    cur.execute(
        """CREATE TABLE authors_and_books (
            author_key           text,
            book_key             text
        )"""
    )

    cur.execute(
        """CREATE TABLE authors (
            wikipedia            text,
            key                  text,
            remote_ids           text,
            created              text,
            birth_date           text,
            name                 text,
            latest_revision      text,
            last_modified        text,
            alternate_names      text,
            type                 text,
            photos               text,
            revision             text,
            personal_name        text,
            death_date           text,
            source_records       text,
            id                   text,
            bio                  text,
            links                text,
            title                text,
            data                 text,
            date                 text,
            fuller_name          text,
            location             text
        )"""
    )

    cur.execute(
        """CREATE TABLE books (
            subtitle                      text,
            authors                       text,
            title                         text,
            publishers                    text,
            number_of_pages               text,
            physical_format               text,
            notes                         text,
            works                         text,
            publish_date                  text,
            isbn_10                       text,
            covers                        text,
            full_title                    text,
            isbn_13                       text,
            last_modified                 text,
            created                       text,
            type                          text,
            key                           text,
            latest_revision               text,
            revision                      text,
            source_records                text,
            name                          text,
            id                            text,
            publish_places                text,
            identifiers                   text,
            pagination                    text,
            classifications               text,
            copyright_date                text,
            table_of_contents             text,
            contributors                  text,
            edition_name                  text,
            oclc_numbers                  text,
            languages                     text,
            other_titles                  text,
            subjects                      text,
            links                         text,
            subject_places                text,
            description                   text,
            subject_times                 text,
            excerpts                      text,
            subject_people                text,
            series                        text,
            lc_classifications            text,
            first_publish_date            text,
            dewey_number                  text,
            physical_dimensions           text,
            first_sentence                text,
            weight                        text,
            translation_of                text,
            by_statement                  text,
            translated_from               text,
            dewey_decimal_class           text,
            ocaid                         text,
            location                      text,
            publish_country               text,
            personal_name                 text
        )"""
    )
    con.commit()
    con.close()
