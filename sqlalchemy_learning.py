import sqlalchemy
import uuid

from sqlalchemy import Table, Column, String, Integer
from sqlalchemy import MetaData, select, insert, update, delete, func

engine = sqlalchemy.create_engine('sqlite:///test.db', echo=True)


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
    count_stmt = select(func.count()).select_from(algotest)
    result = conn.execute(count_stmt)

    row_count = result.scalar()

    if row_count == 0:
        conn.execute(
            insert(algotest),
            [
                {
                    "id": str(uuid.uuid4()),
                    "algo_name": "binary search",
                    "step": 100,
                    "n_max": 10000
                },
                {
                "id": str(uuid.uuid4()),
                "algo_name": "merge sort",
                "step": 50,
                "n_max": 1000 
                },
                {
                "id": str(uuid.uuid4()),
                "algo_name": "bubble sort",
                "step": 100,
                "n_max": 1000
                }
            ]
        )

        print("Sample data inserted")
    else:
        print("Table already contains data. Skipping INSERT.")

   
    # select
    stmt = select(algotest).where(
        algotest.c.algo_name == "bubble sort",
        algotest.c.n_max > 500
    )

    result = conn.execute(stmt)

    for row in result:
        print(row)


    # update
    stmt = (
        update(algotest).where(algotest.c.algo_name == "bubble sort").values(n_max=2700))

    result = conn.execute(stmt)
    
    print("Rows updated:", result.rowcount)


    # delete
    stmt = delete(algotest).where(
        algotest.c.id == "aa41ad94-b886-4aa0-8a69-64bf9c370fc1"
    )

    result = conn.execute(stmt)

    print("Rows deleted:", result.rowcount)
    conn.commit()