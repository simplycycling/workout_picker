import random
import sqlite3

kb = [
    "week_01_Twister",
    "week_02_Blast",
    "week_03_Gravity",
    "week_04_Elevate",
    "week_05_Breathe",
    "week_06_Lift",
    "week_07_Force",
    "week_08_Heat",
    "week_09_Driven",
    "week_10_Rebellion",
]
core = [
    "week_01",
    "week_02",
    "week_03",
    "week_04",
    "week_05",
    "week_06",
    "week_07",
    "week_08",
    "week_09",
    "week_10",
]


# Set up SQLite database
def setup_database(db_name="selection_counts.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS kb_counts (
        item TEXT PRIMARY KEY,
        count INTEGER DEFAULT 0
    )
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS core_counts (
        item TEXT PRIMARY KEY,
        count INTEGER DEFAULT 0
    )
    """
    )

    # Initialize items in the database if they don't exist
    for item in kb:
        cursor.execute(
            "INSERT OR IGNORE INTO kb_counts (item, count) VALUES (?, 0)", (item,)
        )

    for item in core:
        cursor.execute(
            "INSERT OR IGNORE INTO core_counts (item, count) VALUES (?, 0)", (item,)
        )

    conn.commit()
    return conn


def select_kb(conn):
    cursor = conn.cursor()
    # Randomly select an item from kb list
    random_kb = random.choice(kb)

    # Increment its count in the database
    cursor.execute(
        "UPDATE kb_counts SET count = count + 1 WHERE item = ?", (random_kb,)
    )
    conn.commit()

    return random_kb


def select_core(conn):
    cursor = conn.cursor()
    # Randomly select an item from core list
    random_core = random.choice(core)

    # Increment its count in the database
    cursor.execute(
        "UPDATE core_counts SET count = count + 1 WHERE item = ?", (random_core,)
    )
    conn.commit()

    return random_core


def display_counts(conn):
    cursor = conn.cursor()

    print("KB Counts:")
    cursor.execute("SELECT item, count FROM kb_counts ORDER BY item")
    kb_counts = cursor.fetchall()
    for item, count in kb_counts:
        print(f"  {item}: {count}")

    print("\nCore Counts:")
    cursor.execute("SELECT item, count FROM core_counts ORDER BY item")
    core_counts = cursor.fetchall()
    for item, count in core_counts:
        print(f"  {item}: {count}")


def clear_database(conn):
    cursor = conn.cursor()
    # Reset all counts to 0
    cursor.execute("UPDATE kb_counts SET count = 0")
    cursor.execute("UPDATE core_counts SET count = 0")
    conn.commit()
    print("Database counts have been reset to 0")


# Main function
def main():
    # Setup database and establish connection
    conn = setup_database()

    try:
        # Uncomment the next line to clear the database
        # clear_database(conn)
        
        # Select one workout combination
        kb_item = select_kb(conn)
        core_item = select_core(conn)
        print(f"\nSelected Workouts:")
        print(f"KB: {kb_item}")
        print(f"Core: {core_item}")

        # Display current counts
        display_counts(conn)
        print("-" * 30)

    finally:
        # Make sure we close the connection properly
        conn.close()


if __name__ == "__main__":
    main()
