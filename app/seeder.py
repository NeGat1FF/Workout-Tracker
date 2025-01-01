from bs4 import BeautifulSoup
import requests
import psycopg
import os

page = requests.get('https://www.strengthlog.com/exercise-directory/')
content = page.text

soup = BeautifulSoup(content, 'html.parser')

headers = soup.find_all('h3', class_='wp-block-heading')
lists = soup.find_all('ol', class_='wp-block-list')

MIGRATIONS_FOLDER = "db/migrations"


def run_migrations(cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS schema_migrations (id TEXT PRIMARY KEY)")
    cursor.execute("SELECT id FROM schema_migrations")
    applied_migrations = {row[0] for row in cursor.fetchall()}

    migrations = sorted(os.listdir(MIGRATIONS_FOLDER))
    migrations = [m for m in migrations if m.endswith(".up.sql")]

    for migration in migrations:
        migration_id = migration.split('.')[0]
        if migration_id not in applied_migrations:
            with open(os.path.join(MIGRATIONS_FOLDER, migration)) as f:
                print(f"Applying migration: {migration_id}")
                cursor.execute(f.read())
                cursor.execute("INSERT INTO schema_migrations (id) VALUES (%s)", (migration_id,))

    conn.commit()

with psycopg.connect(os.getenv("DATABASE_URL")) as conn:
    with conn.cursor() as cur:
        run_migrations(cur)

        for header, list in zip(headers, lists):
            muscle_group = str(header.text)
            if muscle_group.endswith('Exercises'):
                muscle_group_id = cur.execute("INSERT INTO muscle_groups (name) VALUES (%s) RETURNING muscle_group_id", (muscle_group.removesuffix(" Exercises"),)).fetchone()[0]
                conn.commit()

                print(f"Muscle Group: {muscle_group.removesuffix(' Exercises')}")

                exercises = list.find_all('a')
                for exercise in exercises:
                    exercise_page = requests.get(exercise['href'])
                    exercise_content = exercise_page.text

                    exercise_soup = BeautifulSoup(exercise_content, 'html.parser')

                    exercise_description = exercise_soup.find('div', class_='wp-block-columns is-layout-flex wp-container-core-columns-is-layout-1 wp-block-columns-is-layout-flex')

                    description_text = '\n'.join(exercise_description.stripped_strings)

                    exercise_id = cur.execute("INSERT INTO exercises (name, description) VALUES (%s, %s) RETURNING exercise_id", (exercise.text, description_text)).fetchone()[0]
                    conn.commit()

                    cur.execute("INSERT INTO exercise_muscle_groups (exercise_id, muscle_group_id) VALUES (%s, %s)", (exercise_id, muscle_group_id))
                    conn.commit()

                print(f"Added {len(exercises)} exercises")
            
            
            
