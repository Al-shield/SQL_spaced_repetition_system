SELECT * FROM df_meetings_persons ldf
INNER JOIN df_meetings_persons rdf
USING (meeting_id)
WHERE ldf.person_name == 'Benjamin'
AND rdf.person_name != 'Benjamin'
