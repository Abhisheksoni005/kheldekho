from pydantic import BaseModel


class RacquetSport(BaseModel):


    athlete_a1 = Athlete(id=contestant_a1_id, name=contestant_a1_name)
    athlete_a2 = Athlete(id=contestant_a2_id, name=contestant_a2_name)
    athlete_b1 = Athlete(id=contestant_b1_id, name=contestant_b1_name)
    athlete_b2 = Athlete(id=contestant_b2_id, name=contestant_b2_name)

    squad_a = Squad(id=contestant_a1_nationality_id,
                    name=contestant_a1_nationality,
                    size=2,
                    athletes=[athlete_a1, athlete_a2])

    squad_b = Squad(id=contestant_b1_nationality_id,
                    name=contestant_b1_nationality,
                    size=2,
                    athletes=[athlete_b1, athlete_b2])

    athlete_a = Athlete(id=contestant_a_id, name=contestant_a_name)
    athlete_b = Athlete(id=contestant_b_id, name=contestant_b_name)

    squad_a = Squad(id=contestant_a_nationality_id,
                    name=contestant_a_nationality,
                    size=1,
                    athletes=[athlete_a])

    squad_b = Squad(id=contestant_b_nationality_id,
                    name=contestant_b_nationality,
                    size=1,
                    athletes=[athlete_b])




