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
        animal = Animal(row['name'], row['date_of_birth'], row['type'], owner, vet, row['treatment_notes'])
        animals.append(animal)
    return(animals)
