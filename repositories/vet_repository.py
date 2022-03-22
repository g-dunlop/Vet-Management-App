import pdb
from db.run_sql import run_sql
from datetime import datetime
from models.vet import Vet
from models.animal import Animal
from models.owner import Owner
import repositories.owner_repository as owner_repository

def save(vet):
    sql = "INSERT INTO vets(full_name) VALUES (%s) RETURNING *"
    values = [vet.full_name]
    results = run_sql(sql, values)
    vet.id = results[0]['id']
    return vet


def delete_all():
    sql = "DELETE FROM vets"
    run_sql(sql)


def select_all():

    vets = []

    sql = "SELECT * FROM vets"
    results = run_sql(sql)
    for row in results:
        vet = Vet(row['full_name'], row['id'])
        vets.append(vet)
    # vets.sort()
    return vets

def sort():
    vets = []

    sql = "SELECT * FROM vets"
    results = run_sql(sql)
    for row in results:
        vet = Vet(row['full_name'], row['id'])
        vets.append(vet)
    vets.sort()
    return vets

def select(id):
    vet = None
    sql = "SELECT * FROM vets WHERE id = %s"
    values = [id]
    result = run_sql(sql, values)[0]
    if result is not None:
        vet = Vet(result['full_name'], result['id'])
    return vet

def delete(id):
    sql = "DELETE FROM vets WHERE id = %s"
    values = [id]
    run_sql(sql, values)


def update(vet):
    sql = "UPDATE vets SET (full_name) = (%s) WHERE id = %s"
    values = [vet.full_name, vet.id]
    run_sql(sql, values)

def animals(vet):
    animals = []
    sql = "SELECT animals.* FROM animals INNER JOIN vets ON animals.vet_id = vets.id WHERE vet_id = %s"
    values = [vet.id]
    results = run_sql(sql, values)
    for row in results:
        animal = Animal(row['name'], row['date_of_birth'], row['type'], row['owner_id'], row['vet_id'], row['treatment_notes'], row['id'])
        # animal.date_of_birth = datetime.strptime(animal.date_of_birth, ("%Y-%m-%d"))
        # animal.date_of_birth = animal.date_of_birth.strftime("%d/%m/%Y")
        animals.append(animal)
    return animals

# def appointments(vet):
#     appointments = []
#     sql = "SELECT appointments.* FROM appointments INNER JOIN vets ON appointments.animals.vet_id = vets.id WHERE vet_id = %s"

def count_animals(vet):
    animals = []
    sql = "SELECT animals.* FROM animals INNER JOIN vets ON animals.vet_id = vets.id WHERE vet_id = %s"
    values = [vet.id]
    results = run_sql(sql, values)
    animals_length = 0
    for row in results:
        animal = Animal(row['name'], row['date_of_birth'], row['type'], row['owner_id'], row['vet_id'], row['treatment_notes'], row['id'])
        # animal.date_of_birth = datetime.strptime(animal.date_of_birth, ("%Y-%m-%d"))
        # animal.date_of_birth = animal.date_of_birth.strftime("%d/%m/%Y")
        animals.append(animal)
        animals_length = len(animals)
    return animals_length

def select_by_name(name):
    vets = []
    sql = "SELECT * FROM vets WHERE full_name LIKE %s"
    values = ['%' + name + '%']
    results = run_sql(sql, values)
    
    for row in results:
        vet = Vet(row['full_name'], row['id'])
        vets.append(vet)
    return vets


    # make a join to show appointments

    