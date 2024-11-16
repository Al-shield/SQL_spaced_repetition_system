WITH meetings AS (
    SELECT 
        meeting_id, 
        t1.person_name AS person_left, 
        t2.person_name AS person_right, 
        t1.duration_minutes
    FROM df_meetings_persons t1
        JOIN df_meetings_persons t2 USING(meeting_id)
    WHERE 1=1
        AND t1.person_name == 'Benjamin' 
        AND t2.person_name != 'Benjamin'
)

SELECT person_right, AVG(duration_minutes) AS moyenne
FROM meetings
GROUP BY person_right
HAVING moyenne > 60