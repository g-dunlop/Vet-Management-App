from db.run_sql import run_sql

from models.animal import Animal
from models.owner import Owner
from models.vet import Vet

import repositories.owner_repository as owner_repository
import repositories.vet_repository as vet_repository

def save(animal):
    sql = "INSERT INTO animals (name, date_of_birth, type, owner_id, vet_id, treatment_notes) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *"
    values = [animal.name, animal.date_of_birth, animal.type, animal.owner.id, animal.vet.id, animal.treatment_notes]
    results = run_sql(sql, values)
    animal.id = results[0]['id']
    return animal


def delete_all():
    sql = "DELETE FROM animals"
    run_sql(sql)

def select_all():
    animals = []
    sql = "SELECT * FROM animals"
    results = run_sql(sql)

    for row in results:
        owner = owner_repository.select(row['owner_id'])
        vet = vet_repository.select(row['vet_id'])
        animal = Animal(row['name'], row['date_of_birth'], row['type'], owner, vet, row['treatment_notes'], row['id'])
        animals.append(animal)
    return(animals)

def delete(id):
    sql = "DELETE FROM animals WHERE id = %s"
    values = [id]
    run_sql(sql, values)

def update(animal):
    sql = "UPDATE animals SET (name, date_of_birth, type, owner_id, vet_id, treatment_notes) = (%s, %s, %s, %s, %s, %s) WHERE id = %s"
    values = [animal.name, animal.date_of_birth, animal.type, animal.owner.id, animal.vet.id, animal.treatment_notes, animal.id]
    print(values)
    run_sql(sql, values)

def select(id):
    animal = None
    sql = "SELECT * FROM animals WHERE id = %s"
    values = [id]
    result = run_sql(sql, values)[0]

    if result is not None:
        owner = owner_repository.select(result['owner_id'])
        vet = vet_repository.select(result['vet_id'])
        animal = Animal(result['name'], result['date_of_birth'], result['type'], owner, vet, result['treatment_notes'], result['id'])
    return animal


def select_by_name(name):
    result = None
    sql = "SELECT * FROM animals WHERE name LIKE %s"
    values = [name]
    result = run_sql(sql, values)[0]
    
    if result is not None:
        vet = vet_repository.select(result['vet_id'])
        owner = owner_repository.select(result['owner_id'])        
        animal = Animal(result['name'], result['date_of_birth'], result['type'], owner, vet, result['treatment_notes'], result['id'])

    return animal