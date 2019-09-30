SELECT RANK()
    OVER (
        ORDER BY sos DESC
    ) sos_rank, name, sos
    FROM Teams;