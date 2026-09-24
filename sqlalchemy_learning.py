import sqlalchemy
import uuid

engine = sqlalchemy.create_engine('sqlite:///test.db', echo=True)

with engine.connect() as conn:
    conn.execute(sqlalchemy.text("""
    create table if not exists algotest (
    id varchar(36) primary key,
    algo_name varchar(100) not null,
    step int not null,
    n_max int not null
    )
    """
    ))


    # conn.execute(sqlalchemy.text("""
    #     insert into algotest (
    #     id,
    #     algo_name,
    #     step,
    #     n_max
    #     )
    #     values (
    #     :id,
    #     :algo_name,
    #     :step,
    #     :n_max
    #     )
    #     """),
    #     [
    #         {
    #             "id": str(uuid.uuid4()),
    #             "algo_name": "binary search",
    #             "step": 1,
    #             "n_max": 100

    #         },
    #         {
    #         "id": str(uuid.uuid4()),
    #             "algo_name": "merge sort",
    #             "step": 20,
    #             "n_max": 100 
    #         },
    #         {
    #             "id": str(uuid.uuid4()),
    #             "algo_name": "bubble sort",
    #             "step": 100,
    #             "n_max": 1000
    #         }
    #     ]
    # )
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

    conn.execute(sqlalchemy.text("""
        update algotest
        set n_max = :new_n_max
        where algo_name = :algo_name
    """),
    {
        "new_n_max": 10000,
        "algo_name": "binary search"
    }
    )

    conn.commit()