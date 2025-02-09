import sqlite3

# Połączenie z bazą danych
conn = sqlite3.connect('users.db')

# Ustawienie konwertera wyników na słowniki
conn.row_factory = sqlite3.Row

# Tworzenie kursora
cursor = conn.cursor()

# Wykonanie zapytania SQL
cursor.execute("SELECT * FROM users")

# Pobranie wszystkich wyników
rows = cursor.fetchall()

# Przekształcenie wyników na listę słowników
dict_rows = [dict(row) for row in rows]

# Zamknięcie połączenia
conn.close()

# Wyświetlenie wyników
print(dict_rows)
