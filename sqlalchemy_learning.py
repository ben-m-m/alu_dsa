import sqlalchemy
import uuid

from sqlalchemy import Table, Column, String, Integer
from sqlalchemy import MetaData, select, insert, update, delete

engine = sqlalchemy.create_engine('sqlite:///test.db', echo=True)

# with engine.connect() as conn:
#     conn.execute(sqlalchemy.text("""
#     create table if not exists algotest (
#     id varchar(36) primary key,
#     algo_name varchar(100) not null,
#     step int not null,
#     n_max int not null
#     )
#     """
#     ))
metadata = MetaData()

algotest = Table(
    "algotest",
    metadata,
    Column("id", String(36), primary_key=True),
    Column("algo_name", String(100), nullable=False),
    Column("step", Integer, nullable=False),
    Column("n_max", Integer, nullable=False)
)

metadata.create_all(engine)

with engine.connect() as conn:

    # Insert
    conn.execute(
        insert(algotest),
        [
            {
                "id": str(uuid.uuid4()),
                "algo_name": "binary search",
                "step": 1,
                "n_max": 100
            },
            {
            "id": str(uuid.uuid4()),
            "algo_name": "merge sort",
            "step": 20,
            "n_max": 100 
            },
            {
            "id": str(uuid.uuid4()),
            "algo_name": "bubble sort",
            "step": 100,
            "n_max": 1000
            }
        ]
    )
    result = conn.execute(sqlalchemy.text("""
        select * from algotest 
        where algo_name = :algo_name
        and step = :step
    """),
    {
        "algo_name": "merge sort",
        "step": 20
    }
    )

    for row in result:
    # row = result.fetchone()
    # print("ID:", row.id)
    # print("Algorithm:", row.algo_name)
    # print("Step:", row.step)
    # print("N max:", row.n_max)
        print(row)

    result = conn.execute(sqlalchemy.text("""
        update algotest
        set n_max = :new_n_max
        where algo_name = :algo_name
    """),
    {
        "new_n_max": 2700,
        "algo_name": "bubble sort"
    }
    )
    print("Rows updated:", result.rowcount)

    # result = conn.execute(
    #     sqlalchemy.text("""
    #     select * from algotest
    #     where algo_name = :algo_name
    #     """),
    #     {"algo_name": "bubble sort"}
    # )
    # for row in result:
    #     print(row)

    result = conn.execute(
        sqlalchemy.text("""
    delete from algotest
    where id = :id
    """),
        {"id": "aa41ad94-b886-4aa0-8a69-64bf9c370fc1"}
    )
    print("Rows deleted:", result.rowcount)
    conn.commit()